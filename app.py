import streamlit as st
import time
from ec2_launcher import (
    get_latest_ubuntu_ami, launch_instance,
    get_key_pairs, get_security_groups, get_subnets, get_iam_roles,
    get_recent_ubuntu_amis, get_recent_amazon_linux_amis,
    get_recent_rhel_amis, get_recent_windows_amis, get_recent_macos_amis,
    create_key_pair, stop_instance, terminate_instance
)
try:
    from streamlit_lottie import st_lottie
except ImportError:
    st.warning("Install streamlit-lottie for animations: pip install streamlit-lottie")
    st_lottie = None
import requests

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Roboto+Slab:wght@700&family=Lato:wght@700&family=Merriweather:wght@700&display=swap');
    .main-title {font-family: 'Montserrat', sans-serif; font-size: 2.2rem; color: #1abc9c; font-weight: 700; margin-bottom: 0.5em;}
    .section-credentials {font-family: 'Roboto Slab', serif; font-size: 1.3rem; color: #2980b9; font-weight: 700; margin-top: 1.5em;}
    .section-ami {font-family: 'Lato', sans-serif; font-size: 1.2rem; color: #16a085; font-weight: 700; margin-top: 1.5em;}
    .section-keypair, .section-sg, .section-subnet, .section-iam, .section-tags {
        font-family: 'Montserrat', sans-serif; font-size: 1.25rem; font-weight: 700; margin-top: 1.5em; margin-bottom: 0.2em;
    }
    .section-keypair {color: #8e44ad;}
    .section-sg {color: #34495e;}
    .section-subnet {color: #27ae60;}
    .section-iam {color: #c0392b;}
    .section-tags {color: #f39c12;}
    div[data-testid="stMarkdown"] + div > div > div > div {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    div[data-testid="stMarkdown"] span + div,
    div[data-testid="stMarkdown"] span + div > div > div > div {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
''', unsafe_allow_html=True)

lottie_url = "https://assets2.lottiefiles.com/packages/lf20_Stt1Rk.json"
lottie_json = load_lottieurl(lottie_url)

st.set_page_config(page_title="EC2 Instance Launcher", layout="centered")

if st_lottie and lottie_json:
    st_lottie(lottie_json, height=180, key="cloud-anim")

placeholder_title = st.empty()
def animated_typing(text, speed=0.06):
    displayed = ""
    for char in text:
        displayed += char
        placeholder_title.markdown(f"<div class='main-title'>{displayed}</div>", unsafe_allow_html=True)
        time.sleep(speed)
animated_typing("🚀 Interactive EC2 Launcher Panel", speed=0.07)

st.markdown("""
<div style='display:flex;align-items:center;font-family:Montserrat,sans-serif;font-size:1.25rem;font-weight:700;color:#e67e22;margin-top:2em;margin-bottom:0.2em;'>
  <span style='font-size:1.3em;margin-right:0.5em;'>📝</span>Instance Name (will appear as the Name tag)
</div>
""", unsafe_allow_html=True)
instance_name = st.text_input("", placeholder="e.g. my-ec2-instance")

st.markdown("""
<div style='display:flex;align-items:center;font-family:Montserrat,sans-serif;font-size:1.25rem;font-weight:700;color:#2980b9;margin-top:1.5em;margin-bottom:0.2em;'>
  <span style='font-size:1.3em;margin-right:0.5em;'>🔐</span>AWS Credentials ✨
</div>
""", unsafe_allow_html=True)
aws_access_key_id = st.text_input("AWS Access Key ID", type="password", placeholder="Enter your AWS Access Key ID")
aws_secret_access_key = st.text_input("AWS Secret Access Key", type="password", placeholder="Enter your AWS Secret Access Key")
regions = ["ap-south-1", "us-east-1", "eu-central-1"]
region = st.selectbox("🌍 Choose AWS Region", regions)

if not aws_access_key_id or not aws_secret_access_key:
    st.warning("Please enter your AWS credentials to proceed.")
    st.stop()

instance_types = ["t2.micro", "t2.small", "t2.medium", "t3.micro"]
instance_type = st.selectbox("📦 Select Instance Type", instance_types)

def fetch_aws_resources(aws_access_key_id, aws_secret_access_key, region):
    key_pairs = get_key_pairs(aws_access_key_id, aws_secret_access_key, region)
    security_groups = get_security_groups(aws_access_key_id, aws_secret_access_key, region)
    subnets = get_subnets(aws_access_key_id, aws_secret_access_key, region)
    iam_roles = get_iam_roles(aws_access_key_id, aws_secret_access_key, region)
    return key_pairs, security_groups, subnets, iam_roles

key_pairs, security_groups, subnets, iam_roles = fetch_aws_resources(
    aws_access_key_id, aws_secret_access_key, region
)

st.markdown("""
<div style='display:flex;align-items:center;font-family:Montserrat,sans-serif;font-size:1.25rem;font-weight:700;color:#16a085;margin-top:1.5em;margin-bottom:0.2em;'>
  <span style='font-size:1.3em;margin-right:0.5em;'>🖼️</span>AMI Selection ✨
</div>
""", unsafe_allow_html=True)
st.markdown("<span style='font-size:0.98rem;color:#b2bec3;'>Select the type of AMI you want to use</span>", unsafe_allow_html=True)
ami_type = st.selectbox(
    "Select AMI Type",
    ["RHEL", "Amazon Linux 2", "Windows", "macOS", "Manual Entry (Other)"]
)
ami_id = ""
if ami_type == "RHEL":
    rhel_amis = get_recent_rhel_amis(aws_access_key_id, aws_secret_access_key, region)
    if rhel_amis:
        ami_options = [f"{ami['Name']} ({ami['ImageId']})" for ami in rhel_amis]
        ami_choice = st.selectbox("Choose RHEL AMI", ami_options)
        ami_id = rhel_amis[ami_options.index(ami_choice)]["ImageId"]
    else:
        st.error("No RHEL AMIs found in this region.")
elif ami_type == "Amazon Linux 2":
    amazon_amis = get_recent_amazon_linux_amis(aws_access_key_id, aws_secret_access_key, region)
    if amazon_amis:
        ami_options = [f"{ami['Name']} ({ami['ImageId']})" for ami in amazon_amis]
        ami_choice = st.selectbox("Choose Amazon Linux 2 AMI", ami_options)
        ami_id = amazon_amis[ami_options.index(ami_choice)]["ImageId"]
    else:
        st.error("No Amazon Linux 2 AMIs found in this region.")
elif ami_type == "Windows":
    windows_amis = get_recent_windows_amis(aws_access_key_id, aws_secret_access_key, region)
    if windows_amis:
        ami_options = [f"{ami['Name']} ({ami['ImageId']})" for ami in windows_amis]
        ami_choice = st.selectbox("Choose Windows AMI", ami_options)
        ami_id = windows_amis[ami_options.index(ami_choice)]["ImageId"]
    else:
        st.error("No Windows AMIs found in this region.")
elif ami_type == "macOS":
    macos_amis = get_recent_macos_amis(aws_access_key_id, aws_secret_access_key, region)
    if macos_amis:
        ami_options = [f"{ami['Name']} ({ami['ImageId']})" for ami in macos_amis]
        ami_choice = st.selectbox("Choose macOS AMI", ami_options)
        ami_id = macos_amis[ami_options.index(ami_choice)]["ImageId"]
    else:
        st.error("No macOS AMIs found in this region.")
else:
    ami_id = st.text_input("Enter AMI ID", placeholder="e.g. ami-0abcdef1234567890")

st.markdown("""
<div style='display:flex;align-items:center;font-family:Montserrat,sans-serif;font-size:1.25rem;font-weight:700;color:#8e44ad;margin-top:1.5em;margin-bottom:0.2em;'>
  <span style='font-size:1.3em;margin-right:0.5em;'>🔑</span>Key Pair Name
</div>
""", unsafe_allow_html=True)
st.markdown("<span style='font-size:0.98rem;color:#b2bec3;'>Select an existing key pair or create a new one</span>", unsafe_allow_html=True)
key_pair_options = key_pairs + ["Create new key pair..."]
key_name = st.selectbox("", key_pair_options)
new_key_material = None
if key_name == "Create new key pair...":
    new_key_name = st.text_input("Enter new key pair name", placeholder="e.g. my-keypair")
    if st.button("Create Key Pair"):
        if new_key_name:
            try:
                new_key_material = create_key_pair(aws_access_key_id, aws_secret_access_key, region, new_key_name)
                st.success(f"Key pair '{new_key_name}' created successfully!")
                st.download_button(
                    label="Download PEM file",
                    data=new_key_material,
                    file_name=f"{new_key_name}.pem",
                    mime="application/x-pem-file"
                )
                key_name = new_key_name
            except Exception as e:
                st.error(f"Failed to create key pair: {e}")
        else:
            st.warning("Please enter a key pair name.")

st.markdown("""
<div style='display:flex;align-items:center;font-family:Montserrat,sans-serif;font-size:1.25rem;font-weight:700;color:#34495e;margin-top:1.5em;margin-bottom:0.2em;'>
  <span style='font-size:1.3em;margin-right:0.5em;'>🛡️</span>Security Groups
</div>
""", unsafe_allow_html=True)
st.markdown("<span style='font-size:0.98rem;color:#b2bec3;'>Select one or more security groups for your instance</span>", unsafe_allow_html=True)
selected_sgs = st.multiselect(
    "", [f"{sg['GroupName']} ({sg['GroupId']})" for sg in security_groups]
)
security_group_ids = [sg['GroupId'] for sg in security_groups if f"{sg['GroupName']} ({sg['GroupId']})" in selected_sgs]

st.markdown("""
<div style='display:flex;align-items:center;font-family:Montserrat,sans-serif;font-size:1.25rem;font-weight:700;color:#27ae60;margin-top:1.5em;margin-bottom:0.2em;'>
  <span style='font-size:1.3em;margin-right:0.5em;'>🌐</span>Subnet
</div>
""", unsafe_allow_html=True)
st.markdown("<span style='font-size:0.98rem;color:#b2bec3;'>Select a subnet for your instance</span>", unsafe_allow_html=True)
subnet_display = [f"{sn['SubnetId']} ({sn['CidrBlock']})" for sn in subnets]
subnet_choice = st.selectbox("", ["(Use default subnet)"] + subnet_display) if subnet_display else None
subnet_id = None
if subnet_choice and subnet_choice != "(Use default subnet)":
    subnet_id = subnet_choice.split()[0]

st.markdown("""
<div style='display:flex;align-items:center;font-family:Montserrat,sans-serif;font-size:1.25rem;font-weight:700;color:#c0392b;margin-top:1.5em;margin-bottom:0.2em;'>
  <span style='font-size:1.3em;margin-right:0.5em;'>👤</span>IAM Role (optional)
</div>
""", unsafe_allow_html=True)
st.markdown("<span style='font-size:0.98rem;color:#b2bec3;'>Select an IAM role for your instance (optional)</span>", unsafe_allow_html=True)
iam_role = st.selectbox("", ["None"] + iam_roles)
if iam_role == "None":
    iam_role = None

st.markdown("""
<div style='display:flex;align-items:center;font-family:Montserrat,sans-serif;font-size:1.25rem;font-weight:700;color:#f39c12;margin-top:1.5em;margin-bottom:0.2em;'>
  <span style='font-size:1.3em;margin-right:0.5em;'>🏷️</span>Tags (optional) ✏️
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("Add Tags"):
    tags = []
    for i in range(3):
        key = st.text_input(f"Tag Key {i+1}", key=f"tag_key_{i}", placeholder="e.g. Environment")
        value = st.text_input(f"Tag Value {i+1}", key=f"tag_value_{i}", placeholder="e.g. Production")
        if key and value:
            tags.append({"Key": key, "Value": value})

if instance_name:
    tags = [tag for tag in tags if tag["Key"] != "Name"]
    tags.insert(0, {"Key": "Name", "Value": instance_name})

st.markdown("""
<div style='display:flex;align-items:center;font-family:Montserrat,sans-serif;font-size:1.25rem;font-weight:700;color:#2c3e50;margin-top:1.5em;margin-bottom:0.2em;'>
  <span style='font-size:1.3em;margin-right:0.5em;'>⚙️</span>Advanced Options 🛠️
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
user_data = st.text_area("User Data (optional)", placeholder="#!/bin/bash\necho Hello World > /home/ec2-user/hello.txt")
volume_size = st.number_input("Root Volume Size (GB)", min_value=8, max_value=2000, value=8)
volume_type = st.selectbox("Root Volume Type", ["gp2", "gp3", "io1", "io2", "sc1", "st1"])

if st.button("🚀 Launch Instance"):
    if not ami_id:
        st.error("❌ Please provide a valid AMI ID.")
    elif key_name == "Create new key pair...":
        st.error("❌ Please create and download your new key pair before launching.")
    else:
        status_placeholder = st.empty()
        with st.spinner("Launching EC2 Instance..."):
            for msg in ["Contacting AWS...", "Preparing launch parameters...", "Launching instance..."]:
                status_placeholder.info(msg)
                time.sleep(0.7)
            info = launch_instance(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region=region,
                instance_type=instance_type,
                ami_id=ami_id,
                key_name=key_name,
                security_group_ids=security_group_ids if security_group_ids else None,
                subnet_id=subnet_id if subnet_id else None,
                iam_instance_profile=iam_role,
                user_data=user_data if user_data else None,
                volume_size=int(volume_size),
                volume_type=volume_type,
                tags=tags if tags else None
            )
            status_placeholder.empty()
            if "Error" in info:
                st.error(f"❌ {info['Error']}")
            else:
                st.success("✅ Instance Launched Successfully!")
                st.balloons()
                st.session_state['last_instance'] = info

last_instance = st.session_state.get('last_instance')
if last_instance and 'Instance ID' in last_instance:
    lottie_success = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_kkflmtur.json")
    if st_lottie and lottie_success:
        st_lottie(lottie_success, height=100, key="success-checkmark")
    st.markdown(
        f'''
        <div style="background: linear-gradient(90deg, #e0eafc 0%, #cfdef3 100%); border-radius: 16px; padding: 1.5em; margin-top: 1em; box-shadow: 0 4px 16px rgba(44,62,80,0.08);">
            <h3 style="color:#1abc9c; font-family:Montserrat, sans-serif; margin-bottom:0.5em;">🎉 Instance Details</h3>
            <p><b>🆔 Instance ID:</b> <span style="color:#34495e;">{last_instance.get('Instance ID','')}</span></p>
            <p><b>💡 State:</b> <span style="color:#27ae60;">{last_instance.get('State','')}</span></p>
            <p><b>🖥️ Type:</b> {last_instance.get('Type','')}</p>
            <p><b>🌐 Public IP:</b> <span style="color:#2980b9;">{last_instance.get('Public IP','')}</span></p>
            <p><b>🖼️ AMI:</b> {last_instance.get('AMI','')}</p>
        </div>
        ''',
        unsafe_allow_html=True
    )
    st.write(":blue[Copy Instance ID]:")
    st.code(last_instance.get('Instance ID', ''), language='text')
    if last_instance.get('Public IP'):
        st.write(":blue[Copy Public IP]:")
        st.code(last_instance.get('Public IP', ''), language='text')
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛑 Stop Instance", key="stop_instance_btn"):
            try:
                stop_instance(aws_access_key_id, aws_secret_access_key, region, last_instance.get('Instance ID',''))
                st.success("Instance stop initiated.")
            except Exception as e:
                st.error(f"Failed to stop instance: {e}")
    with col2:
        if st.button("❌ Terminate Instance", key="terminate_instance_btn"):
            try:
                terminate_instance(aws_access_key_id, aws_secret_access_key, region, last_instance.get('Instance ID',''))
                st.success("Instance termination initiated.")
            except Exception as e:
                st.error(f"Failed to terminate instance: {e}")
