# 🚀 EC2 Instance Launcher Panel

An interactive and intuitive **Streamlit-based web app** that simplifies the process of launching, stopping, and terminating AWS EC2 instances using your own credentials. This tool is designed to be beginner-friendly, yet powerful enough for developers and cloud engineers who want granular control over their EC2 configurations.

<img width="1526" height="1012" alt="image" src="https://github.com/user-attachments/assets/53140648-a9c2-42f0-b4f2-f911dad2bfb9" />

---

### Try App - https://ec2-instance-launcher.streamlit.app/

## ✨ Features

- 🔑 Secure AWS Credential Input
- 📦 Customizable EC2 Launch Parameters:
  - Choose AMIs: RHEL, Amazon Linux, Windows, macOS, or custom
  - Select instance type, subnet, security groups, IAM roles
  - Add optional tags, user data, and volume specs
- 🛡️ Key Pair Management: create & download PEM files
- 📊 Live Status Updates during launch
- ✅ Visual success confirmation with instance details
- 🛑 Stop / ❌ Terminate your instance in one click
- 🎨 Modern, animated UI with typing effects and Lottie visuals

---

## 📸 App Preview

> The app guides users step-by-step to configure an EC2 instance with a beautiful UI and real-time feedback. Includes animations and modern typography for an engaging experience.

---

## 🧠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python (Boto3 API calls)
- **UI Enhancements**: Lottie Animations, Google Fonts, Typing Animations
- **Cloud**: AWS EC2 (via IAM access)

---

## 🛠️ Installation & Usage

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ec2-launcher-panel.git
cd ec2-launcher-panel

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py
```
## 🔐 Credentials Notice

This app **requires your personal AWS credentials** (`Access Key ID` and `Secret Access Key`) to function. These are used **only within your current Streamlit session** and are not stored, logged, or transmitted elsewhere.

> ⚠️ Always keep your credentials secure. Do **not** share or hardcode them into public repositories.

---

## 📂 Directory Structure

```bash
ec2-launcher-panel/
│
├── app.py                 # Main Streamlit application
├── ec2_launcher.py        # Core logic to interact with AWS EC2 services
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```
