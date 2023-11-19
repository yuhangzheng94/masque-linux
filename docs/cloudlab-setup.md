# CloudLab Setup
1. Go to https://www.cloudlab.us/ and log in.
2. Start experiment. In Step 2 "Parameterize", set the following:
```json
    Number of Nodes: 3,
    Select OS image: UBUNTU 22.04,
    (Advanced) Temporary Filesystem Size: 10
```
3. Click on each node and select "Shell". For the sake of convenience, use `Remote - SSH` extension in VS Code.
4. On each node, run `sudo apt update`.