import tidalapi
import webbrowser
from pathlib import Path

SESSION_FILE = Path("tidal_session.json")

def authorize_tidal() -> tidalapi.Session:
    session = tidalapi.Session()
    session.load_session_from_file(SESSION_FILE)

    if session.check_login():
        print("[Auth] Session is valid, no need to reauthorize.")
        return session

    login_link, future = session.login_oauth()
    webbrowser.open("https://" + login_link.verification_uri_complete)
    print("[Auth] Waiting for authorization...")

    try:
        future.result()
        print("[Auth] Logged in successfully!")
    except Exception as e:
        print(f"[Auth] Authorization failed: {e}")
        raise

    session.save_session_to_file(SESSION_FILE)
    return session

if __name__ == "__main__":
    session = authorize_tidal()