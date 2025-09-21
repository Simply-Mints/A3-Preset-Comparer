from bs4 import BeautifulSoup

def get_mod_list(filename):
    mod_list = []

    with open(filename, encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find all rows inside the div.mod-list
    mod_rows = soup.select("div.mod-list tr[data-type='ModContainer']")
    for row in mod_rows:
        # Display name in td[data-type="DisplayName"]
        display_td = row.find("td", {"data-type": "DisplayName"})
        displayname = display_td.get_text(strip=True) if display_td else None

        # Link in td containing <a data-type="Link">
        link_a = row.find("a", {"data-type": "Link"})
        link = link_a.get_text(strip=True) if link_a else None

        if displayname and link:
            mod_list.append({
                "DisplayName": displayname,
                "Link": link
            })

    return mod_list