<!-- Improved compatibility of back to top link - https://github.com/othneildrew/Best-README-Template -->
<a id="readme-top"></a>

<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">


  <h3 align="center">CodeDocuAI</h3>

  <p align="center">
    Transform your code into beautiful documentation with AI
    <br />
    <a href="https://github.com/masoningithub/CodeDocuAI"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/masoningithub/CodeDocuAI/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/masoningithub/CodeDocuAI/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project


CodeDocuAI is an intelligent code documentation generator that transforms your source code into comprehensive Software Design Documents (SDD), interactive mindmaps, and summaries using advanced AI. Built with a beautiful modern interface, it supports multiple API providers and offers various documentation templates with dynamic configuration.

Here's why CodeDocuAI stands out:
* **Multi-file Analysis**: Process multiple code files simultaneously with real-time progress tracking
* **AI-Powered Documentation**: Generate comprehensive SDDs using advanced language models from multiple providers
* **Interactive Mindmaps**: Create beautiful, interactive mindmaps with MarkMap integration including expand/collapse controls
* **Professional Templates**: Choose from specialized SDD templates for different project types
* **Modern Interface**: Beautiful gradient design with responsive layout and smooth animations

Of course, no one tool will serve all documentation needs since your requirements may vary. But CodeDocuAI provides a solid foundation that you can build upon and customize for your specific needs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

This section lists the major frameworks/libraries used to bootstrap CodeDocuAI:

* [![Streamlit][Streamlit.io]][Streamlit-url]
* [![Python][Python.org]][Python-url]
* [![OpenAI][OpenAI.com]][OpenAI-url]
* [![MarkMap][MarkMap.js]][MarkMap-url]
* [![D3][D3js.org]][D3-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Before you begin, ensure you have the following installed:
* Python 3.8 or higher
* pip package manager
* A modern web browser
* API key from one of the supported providers (OpenAI, DeepSeek, Aliyun, etc.)

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/masoningithub/CodeDocuAI.git
   ```

2. **Navigate to the project directory**
   ```sh
   cd codedocuai
   ```

3. **Install Python dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables (Optional)**
   ```sh
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```sh
   streamlit run main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

#### Alternative: Docker Installation

1. **Clone and navigate to directory**
   ```sh
   git clone https://github.com/masoningithub/CodeDocuAI.git
   cd codedocuai
   ```

2. **Build and run with Docker Compose**
   ```sh
   docker-compose up -d
   ```

3. **Access the application**
   Open `http://localhost:8501` in your browser

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

CodeDocuAI provides an intuitive interface for generating documentation from your code. Here's how to use it:

### 1. Configure API Settings
Choose your preferred AI provider and enter your API credentials:
- **OpenAI**: Premium quality with GPT-4
- **DeepSeek**: Best balance of cost and performance (recommended)
- **Aliyun**: Great for users in China
- **Volcengine**: Enterprise-focused
- **SiliconFlow**: Latest model access

### 2. Select Documentation Template
Choose from specialized templates:
- **Standard**: Comprehensive automation template
- **Microservices**: For distributed architectures
- **Web Application**: For web development projects
- **API Service**: For API documentation

### 3. Upload Your Code Files
Supported file types: `.py`, `.js`, `.java`, `.c`, `.cpp`, `.h`, `.md`, `.txt`

### 4. Generate Documentation
Select what to generate:
- **SDD**: Comprehensive Software Design Document
- **Mindmap**: Interactive visual representation
- **Summary**: Concise technical overview

### 5. Explore Results
View and download your generated documentation in multiple formats.

**Example SDD Output:**
```markdown
# Software Design Document

## 1. Overview
### 1.1 Purpose
This document describes the software design for...

## 2. Solution Overview
### 2.1 Solution Feature
The application implements...
```

**Example Mindmap Structure:**
- Project Architecture
  - Frontend Components
    - User Interface
    - State Management
  - Backend Services
    - API Layer
    - Business Logic
  - Database Design

_For more examples, please refer to the [Documentation](https://github.com/masoningithub/CodeDocuAI/wiki)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Multi-file processing with progress tracking
- [x] Interactive mindmaps with expand/collapse controls
- [x] Multiple AI provider support
- [x] Beautiful modern interface with animations
- [x] Professional SDD templates
- [ ] Custom template builder interface
- [ ] Git repository integration
- [ ] Collaborative editing features
- [ ] PDF export functionality
- [ ] Advanced code analysis metrics

See the [open issues](https://github.com/masoningithub/CodeDocuAI/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Setup

For local development:

```sh
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run with hot reload
streamlit run main.py --server.runOnSave true
```


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to:

* [Streamlit](https://streamlit.io/) - Amazing web framework for Python applications
* [MarkMap](https://markmap.js.org/) - Beautiful interactive mindmap visualization
* [OpenAI](https://openai.com/) - Leading AI API for natural language processing
* [DeepSeek](https://www.deepseek.com/) - Cost-effective AI models

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/masoningithub/CodeDocuAI.svg?style=for-the-badge
[contributors-url]: https://github.com/masoningithub/CodeDocuAI/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/masoningithub/CodeDocuAI.svg?style=for-the-badge
[forks-url]: https://github.com/masoningithub/CodeDocuAI/network/members
[stars-shield]: https://img.shields.io/github/stars/masoningithub/CodeDocuAI.svg?style=for-the-badge
[stars-url]: https://github.com/masoningithub/CodeDocuAI/stargazers
[issues-shield]: https://img.shields.io/github/issues/masoningithub/CodeDocuAI.svg?style=for-the-badge
[issues-url]: https://github.com/masoningithub/CodeDocuAI/issues
[license-shield]: https://img.shields.io/github/license/masoningithub/CodeDocuAI.svg?style=for-the-badge
[license-url]: https://github.com/masoningithub/CodeDocuAI/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/yourusername
[product-screenshot]: images/screenshot.png
[Streamlit.io]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[OpenAI.com]: https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white
[OpenAI-url]: https://openai.com/
[MarkMap.js]: https://img.shields.io/badge/MarkMap-4285F4?style=for-the-badge&logo=googlemaps&logoColor=white
[MarkMap-url]: https://markmap.js.org/
[D3js.org]: https://img.shields.io/badge/D3.js-F9A03C?style=for-the-badge&logo=d3.js&logoColor=white
[D3-url]: https://d3js.org/
