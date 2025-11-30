import phoenix as px
import time

try:
    session = px.launch_app()
    print(f"Phoenix launched at: {session.url}")
    # Keep it running for a bit to check
    time.sleep(10)
except Exception as e:
    print(f"Failed to launch Phoenix: {e}")
