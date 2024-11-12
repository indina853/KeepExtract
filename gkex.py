import gkeepapi
import pandas as pd
import re

USERNAME = "YOUR_EMAIL"

keep = gkeepapi.Keep()
token = "YOUR_GPSOAUTH_TOKEN"
keep.resume(USERNAME, token, sync=False)

print("Creating product table...")
keep.sync()
all_notes = keep.all()

filtered_terms = r"(?i)(Códigos? | Xbox(?: One/Xbox Series X\|S/PC| One/Xbox Series X\|S| Series X\|S/PC| Series X\|S| One/PC| 360(?:/Xbox One)?)?| One| PS5| Steam| Rockstar Social Club| PC(?:\sGOG)?|EA App)"

filtered_edition = r"(?i)(Digital|Deluxe|Ultimate|Premium|Cross-gen|Vault|Complete|Definitive|Bundle|Eternal|(FighterZ|Enhanced|Champions|The|Game of|Classic|Gold|Car|Pass|Ten|Year|Pack|Triple|Online|DLC|Legendary|All Madden|Hero|Saga|Starter|Java|&|Bedrock|Michael Jordan|25th|Black Mamba|Kobe Bryant|Gourmet|Special|Remake|Village|Double|Arsenal|Trilogy|Upgrade|Anniversary|Precious|Director's Cut|Master|Vol\. 1|Collection|Legends|Bite Back|Goty|Originals|Chronicles|Zombies|Remastered|Livonia|Add-ons?|Edição Festa|Ezio|VIP|Silver)|(?:Edition)|(?:[-:]))"

data = []

filtered_terms_content = r"(https?://\S+)"

for note in keep.find(labels=None, archived=False):
  if note.pinned:
    title_without_platform = re.sub(filtered_terms, "", note.title)
    edition_match = re.search(filtered_edition, note.title)
    edition = edition_match.group(0) if edition_match else "Standard"
    title_without_edition = re.sub(filtered_edition, "", title_without_platform).strip()
    if any(term in note.title for term in ["Xbox One/Xbox Series X|S", "Xbox One/Xbox Series X|S/PC", "Xbox One/PC", "Xbox 360/Xbox One", "Xbox One"]):
      platform = "Xbox One"
    elif any(term in note.title for term in ["Xbox Series X|S", "Xbox Series X|S/PC"]):
      platform = "Xbox Series"
    else:
      platform = next((p for p in ["Xbox 360", "PS5", "Steam", "Rockstar Social Club", "PC GOG", "PC", "EA App"] if p in note.title), "Outras")
    # edition_match = re.search(filtered_edition, note.title)
    # print(edition_match)
    # edition = edition_match if edition_match else "Standard Edition"        
    urls = re.findall(filtered_terms_content, note.text)
    data.extend({"Product": title_without_edition, "Platform": platform, "Edition": edition, "Purchase link": url}  for url in urls)

df = pd.DataFrame(data).sort_values(by='Product')
df.to_excel("notes.xlsx", index=False)
print("Notes extracted and saved successfully.")