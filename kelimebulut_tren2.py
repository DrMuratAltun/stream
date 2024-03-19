import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Türkçe doğal dil işleme için gerekli veri setlerini indirin
nltk.download('stopwords')
nltk.download('punkt')

def generate_wordcloud(text, language):
    # Metni küçük harflere dönüştürün
    text = text.lower()

    # İngilizce için kök bulma işlemi
    if language == 'İngilizce':
        # Kelimeleri ayıklayın ve İngilizce stop kelimeleri hariç tutun
        words = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

        # Kökleri bulun
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(word) for word in filtered_words]

    # Türkçe için sadece kelime bulutu oluşturma
    else:
        # Kelimeleri ayıklayın ve Türkçe stop kelimeleri hariç tutun
        words = word_tokenize(text, language='turkish')
        stop_words = set(stopwords.words('turkish'))
        filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

        # Kökler ve ekler için ayrı bir işlem yapmıyoruz, sadece kelimeleri kullanıyoruz
        stemmed_words = filtered_words

    # Kelime frekansını hesaplayın
    word_freq = nltk.FreqDist(stemmed_words)

    # Kelime bulutunu oluşturun
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

    # Kelime bulutunu görselleştirin
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

def main():
    st.title("Kök Bulma ve Kelime Bulutu Oluşturma")

    option = st.radio(
        "Metni nasıl girmek istersiniz?",
        ("Metin Yaz", "Dosya Yükle")
    )

    language = st.radio(
        "Dili seçin",
        ("Türkçe", "İngilizce")
    )

    if option == "Metin Yaz":
        text = st.text_area("Metni buraya yazın", height=200)
        if st.button("Kelime Bulutunu Oluştur"):
            if text:
                generate_wordcloud(text, language)
            else:
                st.warning("Lütfen metin girin.")

    elif option == "Dosya Yükle":
        uploaded_file = st.file_uploader("Metin dosyasını yükleyin", type=["txt"])
        if st.button("Kelime Bulutunu Oluştur"):
            if uploaded_file is not None:
                text = uploaded_file.read().decode("utf-8")
                generate_wordcloud(text, language)
            else:
                st.warning("Lütfen bir dosya yükleyin.")

if __name__ == "__main__":
    main()