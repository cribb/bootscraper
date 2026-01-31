import csv

def write_csv_report(page_data, filename="report.csv"):

    fields = ["page_url", "h1", "first_paragraph", "outgoing_link_urls", "image_urls"]

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, restval="NULL")
        writer.writeheader()

        for pagekey in page_data.keys():
            page = page_data[pagekey]
                        
            datarow = {}
            datarow['page_url'] = page['url']
            datarow['h1'] = page['h1']
            datarow['first_paragraph'] = page['first_paragraph']
            datarow['outgoing_link_urls'] = ';'.join(page['outgoing_links'])
            datarow['image_urls']  = ';'.join(page['image_urls'])

            # datarow = [url, h1, fp, links, images]

            # print(f" --> DATA_ROW: {datarow}")
            writer.writerow(datarow)

