# Venture ✨ 🧑‍🚀 ✨ (STILL WIP! KINDLY WAIT TILL WE WRAP THINGS UP, pip NOT YET PUBLISHED)

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
Instead of relying on traditional search techniques, Venture employs a novel approach.

For each document added to the ``Cosmos``, metadata such as file name, summary, and owner is extracted.  
Venture then utilizes the 'function call' feature of ChatGPT to generate dynamic functions based on this metadata.  
By leveraging the reasoning capabilities of ChatGPT, Venture performs a ChatGPT 'function call' with all the docs metadata.

### 🛑 Limitation:
The current version of Reasoning-Based Search in ``Venture`` supports up to approximately 70 documents.  
However, we are actively working on the next version, which will enable support for hundreds of documents in search.  
More details soon.

### 🤔 Why not use embeddings?
While we highly appreciate the usefulness of embeddings, they have certain limitations.  
Embedding-based searches struggle with limited context for short texts and tend to be too noisy for long texts.  
Additionally, Embedding-based search does not provide a clear indication when no relevant results are found.  
Although techniques like thresholds and metadata enhancements can assist, our (humble) research has shown that Reasoning-Based Search, powered by a robust language model like ChatGPT, is a superior searching approach that finds the most relevant docs.

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