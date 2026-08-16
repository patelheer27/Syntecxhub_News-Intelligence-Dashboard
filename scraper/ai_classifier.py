from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Training examples
training_texts = [
    # Technology
    "Apple launches new artificial intelligence technology",
    "Microsoft releases new software and cloud platform",
    "Google develops new AI model",
    "New smartphone processor technology announced",
    "Cybersecurity researchers discover software vulnerability",

    # Business
    "Stock market rises after strong company earnings",
    "Company announces major business investment",
    "Bank increases interest rates",
    "Business leaders discuss economic growth",
    "Startup raises millions in funding",

    # Sports
    "India wins cricket match against Australia",
    "Football team reaches championship final",
    "Tennis player wins major tournament",
    "Olympic athlete breaks world record",
    "Cricket player scores century",

    # Politics
    "Government announces new policy",
    "President meets foreign leaders",
    "Parliament passes new bill",
    "Election campaign begins",
    "Political leaders discuss national issues",

    # Health
    "Doctors discover new treatment for disease",
    "Hospital introduces new medical technology",
    "Scientists develop new vaccine",
    "Health researchers study disease prevention",
    "Government launches public health program",

    # Entertainment
    "New movie breaks box office record",
    "Actor announces upcoming film",
    "Music artist releases new album",
    "Film festival announces winners",
    "Streaming platform launches new series",

    # Science
    "Scientists discover new planet",
    "Researchers study climate change",
    "Space agency launches satellite",
    "Scientists make breakthrough in physics",
    "Astronomers observe distant galaxy",

    # World
    "International leaders meet for global summit",
    "Countries announce new international agreement",
    "United Nations discusses global issues",
    "World leaders respond to international crisis",
    "International community calls for cooperation"
]

training_labels = [
    "Technology", "Technology", "Technology", "Technology", "Technology",
    "Business", "Business", "Business", "Business", "Business",
    "Sports", "Sports", "Sports", "Sports", "Sports",
    "Politics", "Politics", "Politics", "Politics", "Politics",
    "Health", "Health", "Health", "Health", "Health",
    "Entertainment", "Entertainment", "Entertainment", "Entertainment", "Entertainment",
    "Science", "Science", "Science", "Science", "Science",
    "World", "World", "World", "World", "World"
]


# Create TF-IDF model
vectorizer = TfidfVectorizer(
    stop_words="english"
)

X = vectorizer.fit_transform(training_texts)


# Train classifier
model = LogisticRegression(
    max_iter=1000
)

model.fit(X, training_labels)


def predict_category(title):
    """
    Predict the category of a news headline.
    """

    title_vector = vectorizer.transform([title])

    prediction = model.predict(title_vector)

    return prediction[0]


# Test
if __name__ == "__main__":

    test_titles = [
        "New AI technology launched by Google",
        "India wins cricket match",
        "Stock market reaches new high",
        "Scientists discover new planet"
    ]

    for title in test_titles:

        category = predict_category(title)

        print(f"{title}")
        print(f"Category: {category}")
        print("-" * 50)