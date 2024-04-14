class RatesService:

    def __init__(self, connection):
        self.connection = connection

    def _check_port_code(self, slug):
        """
        This method checks whether the provided inputs are specific port codes
        or they can be parent_slug denoting a region
        Returns the parent slug along with child slugs
        """

        slugs = [slug]
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT slug from regions where parent_slug = '{slug}'")
        result = cursor.fetchall()
        if result is not None:
            for row in result:
                slugs.append(row[0])

        if len(slugs) == 1:
            cursor.execute(f"SELECT slug from regions where slug = '{slug}'")
            result = cursor.fetchall()
            if result is None or len(result) == 0:
                slugs = []  # this means that input is a port code and not slug

        cursor.close()
        return slugs

    def get_rates(self, date_from, date_to, origin, destination):
        """
        Returns list of prices for the given date range and ports.
        If instead of port codes, regions are provided, it will return
        the above for all regions and thier child regions
        """

        origin_slugs = self._check_port_code(origin)
        destination_slugs = self._check_port_code(destination)

        cursor = self.connection.cursor()

        if not origin_slugs and not destination_slugs:
            """
            This means that both origin and destination input values
            are port codes
            """
            cursor.execute(f"""SELECT AVG(price), COUNT(price), day FROM prices WHERE
                orig_code='{origin}' AND dest_code='{destination}'
                AND day BETWEEN '{date_from}'AND '{date_to}' GROUP BY day""")

        elif origin_slugs and not destination_slugs:
            """
            This means that destination is port code but origin could be 
            regions and child regions
            """
            cursor.execute(f"""SELECT AVG(price), COUNT(price), day FROM prices JOIN ports on 
                prices.orig_code=ports.code WHERE
                dest_code='{destination}' AND ports.parent_slug in ('{"','".join(origin_slugs)}')
                AND day BETWEEN '{date_from}' AND '{date_to}' GROUP BY day""")

        elif not origin_slugs and destination_slugs:
            """
            This means that origin is port code but destination could be 
            regions and child regions
            """
            cursor.execute(f"""SELECT AVG(price), COUNT(price), day FROM prices JOIN ports on 
                prices.dest_code=ports.code WHERE
                orig_code='{origin}' AND ports.parent_slug in ('{"','".join(destination_slugs)}')
                AND day BETWEEN '{date_from}' AND '{date_to}' GROUP BY day""")
        else:
            """
            This means that both origin and destination could be 
            regions and child regions
            """
            cursor.execute(f"""SELECT AVG(price), COUNT(price), day FROM prices JOIN ports port1 on 
                prices.orig_code=port1.code
                JOIN ports port2 on prices.dest_code=port2.code WHERE port1.parent_slug in ('{"','".join(origin_slugs)}')
                AND port2.parent_slug in ('{"','".join(destination_slugs)}')
                AND day BETWEEN '{date_from}' AND '{date_to}' GROUP BY day""")

        rows = cursor.fetchall()

        rates = list()
        if rows is not None:
            for average_price, count, day in rows:
                if count < 3:
                    average_price = None
                else:
                    average_price = float(average_price)
                rates.append({"day": day.strftime("%Y-%m-%d"), "average_price": average_price})

        cursor.close()
        return rates

