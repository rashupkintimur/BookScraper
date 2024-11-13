import requests, json
from bs4 import BeautifulSoup

url = "https://www.labirint.ru/"

html = requests.get("{0}/{1}".format(url, "books"))
soup = BeautifulSoup(html.text, "html.parser")
links = soup.find("div", {"data-title": "Лучшее"}).find_all("a", {"href": True})

books = []

for link in links:
	href = link.get("href")

	if href:
		htmlBook = requests.get("{0}/{1}".format(url, href))
		soupBook = BeautifulSoup(htmlBook.text, "html.parser")

		bookAuthorTag = soupBook.find("a", {"data-event-label": "author"})

		if bookAuthorTag:
			bookAuthor = bookAuthorTag.getText()
		else:
			bookAuthor = "Автор не найден"

		bookName = soupBook.find("h1").getText()
		bookCost = soupBook.find(class_="buying-priceold-val-number").getText()
		bookRating = soupBook.find(id="rate").getText()
		bookPreviewSrc = soupBook.find(class_="book-img-cover").get("data-src")

		books.append({
			"name": bookName,
			"author": bookAuthor,
			"cost": bookCost,
			"rating": bookRating,
			"previewSrc": bookPreviewSrc
		})

with open("books.json", "w") as file:
	json.dump(books, file, indent=4, ensure_ascii=False)
