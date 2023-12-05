# Switchbot Dashboard

# Requirements
- Docker
- Bluetooth module

# Usage

1. Settings  
Set your Switchbot Bluetooth MAC address in `docker-compose.yaml`.  
    ```yaml
        command: --mac "ab:cd:ef:12:34:56"
    ```

2. Build and start services.  
Execute the following command.  
    ```bash
    $ docker compose up -d
    ```

3. View dashboard  
Access the dashboard `http://localhost:33306`.  
