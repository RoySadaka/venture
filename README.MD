# Venture ✨ 🧑‍🚀 ✨

![](https://raw.githubusercontent.com/RoySadaka/ReposMedia/main/venture/readme/banner.jpg)

## 🚀 Your AI-powered project exploration


``Venture`` let's you to explore and ask questions to your project documentations.  

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/roysadaka.svg?style=social&label=RoySadaka)](https://twitter.com/roysadaka)
![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)
[![PyPI version](https://badge.fury.io/py/venture-ai.svg)](https://badge.fury.io/py/venture-ai) 
[![Downloads](https://pepy.tech/badge/venture-ai)](https://pepy.tech/project/venture-ai)

## For latest PyPI stable release 

```sh
    pip install venture-ai
```

---

## 🛰️ Mission Control
``Venture`` sets out to be a devoted companion for developers and other team members in an organization.  
It serves as an assistant to assist with diverse inquiries concerning projects, protocols, conventions, and any documented details.  
This tool promotes seamless sharing and retrieval of knowledge, fostering teamwork, problem-solving, and collaboration within teams.  
Just like a cosmic entity, ``Venture`` harnesses the power of OpenAI's ChatGPT to embark on this journey.


```python
from venture import Venture

if __name__ == '__main__':
    v = Venture(openai_api_key='sk-...',  # OBTAINED FROM https://platform.openai.com/account/api-keys
                captain_email='captain@spaceship.com',  # THE DEFAULT CONTACT IN INTERLINK TAB 
                extra_role='You are an AI assistant for Venture Company.', # ANY INFO ABOUT YOUR SPECIFIC USE CASE
                share=False) # FOR SHARING THE APP LINK OUTSIDE YOUR LOCAL NETWORK
    v.launch()
```

After initiating the launch, ``Venture``, powered by Gradio, will generate a cosmic link that enables you to activate the application.  
Effortlessly navigate to the bestowed link amidst the vastness of your web browser's galaxy.
```sh
    Running on local URL:  http://127.0.0.1:7860
```

With ``share=True``, you will receive a cosmic link that grants you access to a public space where you can share your project beyond your local network.  
Keep in mind that the mentioned expiration time may vary like distant stars in the galaxy.  
```sh
    Running on public URL: https://3c10d1b4393cd966cd.gradio.live
    This share link expires in 72 hours.
```

---

## 💫 A Cosmic Journey
In the celestial realm of the web app, ``Venture`` unveils its enchanting interface.  
Prepare to embark on a cosmic journey through its three celestial tabs, each designed to guide you through the depths of your project documentation and beyond.

1. 🧑‍🚀 Explore Tab: Unveil the Secrets of the Cosmos
    This ethereal tab serves as your portal to the wonders of project documentation.  
    In it, ``Venture`` eagerly awaits your inquiries and questions.  
    Discover the vast knowledge it holds or let its "Auto-Pilot" feature autonomously guide you to the precise documentation you seek.

2. 🌟 Cosmos Tab: Forge New Stars in the Galaxy
    In this celestial workshop, you possess the power to shape the very fabric of your cosmos.  
    Add new constellations of knowledge to the cosmic expanse or remove existing ones as you navigate through the possibilities of your documentation universe.

3. 📡 Interlink Tab: Communication Across the Stars
    This celestial conduit bridges the gap between you and the support team, ensuring seamless communication amidst the cosmic expanse.  
    Should you encounter enigmatic anomalies or deem a documentation update necessary, harness the power of the Interlink Tab to connect with the support team, who will guide you through the celestial seas of knowledge.

---



## 🔍 Reasoning Based Search
When using 'Auto-Pilot' mode in 📌 Cosmos, ``Venture`` performs a document search.  
Its goal is to find the most suitable document for the user's query.  
Instead of relying on traditional search techniques, ``Venture`` employs a novel approach.

For each document added to the ``Cosmos``, metadata such as file name, summary, and owner is extracted.  
Venture then utilizes the 'function call' feature of ChatGPT to generate dynamic functions based on this metadata.  
By leveraging the reasoning capabilities of ChatGPT, ``Venture`` performs a ChatGPT 'function call' with all the docs metadata.

### 🛑 Limitations:
While ``Venture`` presents a powerful tool for document navigation and search, its current iteration has a few limitations, particularly related to the volume of documents it can effectively handle.

In its present version, Reasoning Based Search in ``Venture`` can effectively support only up to approximately 300 documents.  
A ChatGPT function call for this search method will be triggered for every ~70 documents.  

We're investing our efforts in creating the next version of ``Venture``, which will considerably expand the tool's capabilities to handle search across thousands of documents effectively.  

If you're dealing with a greater volume of documents, we recommend segmenting them and creating multiple instances of ``Venture`` where each instance caters to a specific subset of your documents.


### 🤔 Why no embeddings?
While embeddings are amazing, they also carry certain inherent limitations that influenced our decision not to implement them in ``Venture``. 

* **Limited context for short texts:** Embeddings Based Search can struggle with short texts due to the lack of context, leading to potential inaccuracies in the search results.

* **Noisiness for long texts:** conversely, long texts can introduce too much noise in the embeddings, again resulting in less precise matches.

* **Challenges with Antonyms:** Embeddings often conflate words with opposite meanings, like "good" and "bad", that appear in similar contexts, incorrectly positioning them close together in the vector space.

* **Lack of indication for no relevant results:** one major drawback of Embeddings Based Search methods (like cosine or p2 distance) is their inability to signal when no relevant results are found.  
Though certain techniques like thresholds and metadata enhancements can somewhat ameliorate this issue, the problem remains.

Our (humble) research has led us to the conclusion that a Reasoning Based Search, underpinned by a robust language model like ChatGPT, is more accurate, bypassing the issues raised above.

However, it's important to note that despite its increased accuracy, Reasoning Based Search is much slower than Embeddings Based Search and is not (yet) scalable to thousands of documents in its current form.  


---


## ⚡️ Cosmic Responsibility
You hold the cosmic responsibility for your interactions with ``Venture``, just as you hold the responsibility for handling any powerful tool.  
Sharing any content generated by ``Venture`` is equivalent to sharing it on your own behalf.  
It is important to note that documents containing sensitive information should be avoided as they will be parsed by ChatGPT.  
Exercise caution and ensure that you only include non-sensitive and appropriate content in the documents used with ``Venture``.

---

## 📡 Caught in an interstellar void? Transmit an inquiry!
If you feel that there's something amiss in our celestial realm, we encourage you to reach out. You have a couple of options to connect with us:

1. Open an Issue: If you come across any anomalies or have suggestions for improvements, you can open an issue.  
    Our team will promptly address it and ensure the cosmic balance is restored.

2. Email us: Feel free to send us an email at torch.lpd@gmail.com.  
    We welcome your thoughts, ideas, and any other cosmic communication you wish to share with us.

Together, we can enhance ``Venture`` and embark on an even more remarkable cosmic journey!

---

## 🔭 Stellar Visuals, Unveiling the Interface
Behold these mesmerizing cosmic captures, offering a tantalizing preview of the celestial user interface.  
The version depicted here may exhibit slight variations from the released solutions, akin to the ever-shifting starry night-sky.

#### 🧑‍🚀 Explore Tab
![](https://raw.githubusercontent.com/RoySadaka/ReposMedia/main/venture/readme/explore_ui.jpg)  

---

#### 🌟 Cosmos Tab
![](https://raw.githubusercontent.com/RoySadaka/ReposMedia/main/venture/readme/cosmos_ui.jpg)  

---

#### 📡 Interlink Tab
![](https://raw.githubusercontent.com/RoySadaka/ReposMedia/main/venture/readme/interlink_ui.jpg)  