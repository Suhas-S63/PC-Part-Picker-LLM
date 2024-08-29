# PC Part Picker Bot 🖥️
### Developed By:  Suhas S

🎉 **Welcome to the PC Part Picker Bot!**  
Discover the ultimate assistant for building your dream PC! Whether you're a novice or a tech enthusiast, our bot provides comprehensive insights into PC components, reviews, and comparisons to help you make informed decisions.

## 🚀 Features
- **Discover:** Find the best PC components tailored to your needs.
- **Compare:** Get detailed reviews and side-by-side comparisons of parts.
- **Ask:** Pose any question about PC parts, and receive detailed, helpful answers.
- **Interactive:** Engage with the bot through both text and voice inputs.
- **Advanced Retrieval:** Powered by cutting-edge retrieval-based QA systems for accurate responses.

## 🛠️ How It Works
1. **Load the PDF:** The bot ingests a PDF document containing extensive information about PC hardware.
2. **Text Splitting:** The document is split into manageable chunks for efficient processing.
3. **Vector Embeddings:** We use Pinecone to create a vector store of the document chunks for fast retrieval.
4. **LLM Integration:** A ChatGroq model processes queries based on the context provided by the document.
5. **Custom Prompting:** Tailored prompts guide the LLM to deliver precise and relevant answers.

## 🌟 Getting Started
To get up and running with the PC Part Picker Bot, follow these steps:

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Suhas-S63/PC-Part-Picker-LLM/
    cd pc-part-picker-bot
    ```

2. **Install Dependencies**  
   Make sure you have Python 3.7 or later installed. Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**  
   Create a `.env` file in the root directory and add your environment variables. For example:
    ```env
    PINECONE_API_KEY=your_pinecone_api_key
    CHATGROQ_API_KEY=your_chatgroq_api_key
    ```

4. **Run the Application**
    ```bash
    streamlit run app.py
    ```

5. **Interact with the Bot**  
   Open your browser and navigate to [http://localhost:8501](http://localhost:8501) to start interacting with the PC Part Picker Bot.

## 💡 Future Enhancements
- **Voice Input Support:** Integrate more advanced voice recognition features.
- **Expanded Component Database:** Include more detailed information and reviews on a broader range of components.
- **User Customization:** Allow users to save and compare their own custom PC builds.

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
