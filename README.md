## NetDevOps

This Project is from the book Automating and Orchestrating Networks with NetDevOps

## Notes
The `requirements.txt` file should list all Python libraries that are needed for this project.
Use the following cmd in the CLI to install them:
```
python3 -m install -r requirements.txt
```

## Jenkins Pipeline overview
 ___________________________________
/                                   \
│  Stages                           │
│   ┌──────────────────────────┐    │
│   │ Stage-Build              │    │
│   │  ┌────────────────────┐  │    │
│   │  │ Step: Launch       │  │    │
│   │  │ Docker             │  │    │
│   │  │ container          │  │    │
│   │  └────────────────────┘  │    │
│   │  ┌────────────────────┐  │    │
│   │  │ Step: Copy         │  │    │
│   │  │ ansible code       │  │    │
│   │  │ in container       │  │    │
│   │  │ (git clone)        │  │    │
│   │  └────────────────────┘  │    │
│   └──────────────────────────┘    │
│   ┌──────────────────────────┐    │
│   │ Stage-Test               │    │
│   │  ┌────────────────────┐  │    │
│   │  │ Step: Run unit     │  │    │
│   │  │ tests              │  │    │
│   │  └────────────────────┘  │    │
│   └──────────────────────────┘    │
│   ┌──────────────────────────┐    │
│   │ Stage-Cleanup            │    │
│   │  ┌─────────────────────┐ │    │
│   │  │ Step: Remove Docker │ │    │
│   │  │ container           │ │    │
│   │  └─────────────────────┘ │    │
│   └──────────────────────────┘    │
\___________________________________/
