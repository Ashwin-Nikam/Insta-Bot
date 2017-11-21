import matplotlib.pyplot as plt
from wordcloud import WordCloud


def generate_cloud(tags):
    freq_dict = {}
    for tag in tags:
        freq_dict[tag] = tags.count(tag)
    create_cloud(freq_dict)


def create_cloud(freq_dict):
    wordcloud = WordCloud(background_color='white', width=2000, height=2000)
    wordcloud.generate_from_frequencies(frequencies=freq_dict)
    plt.figure(figsize=(20,10))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()