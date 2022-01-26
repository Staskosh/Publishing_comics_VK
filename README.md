# Publish comics VK

This script allows download and post comics on your own VK group.

### How to install

- Download the code.
- Python3 should be already installed. 
- Install virtual enviriment.
- Create [VK group](https://vk.com/groups).
- Get the group id. You are able to find our it in the URL. 
  For example: `https://vk.com/public210042253` here id is `210042253`.  
  Write it in the file '.env' as
  ```python
  VK_GROUP_ID='here is your group id'
  ```
- Create your own [mini-app](https://vk.com/apps?act=manage). Select the standalone one.
- Get client_id for the mini-app. You are able to find our it in the URL. 
  For example: `https://vk.com/editapp?id=8147012&section=info` here id is `8147012`.
- Get [access_token](https://vk.com/dev/implicit_flow_user) with the following permisions photos, groups, wall, offline.
  Write it in the file '.env' as
  ```python
  VK_ACCESS_TOKEN='here is your access token'
  ```
- Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```python
pip install -r requirements.txt
```

## How to use

1. For downloading and publishing random comics run the script:
```python
python3 publish_comics.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).