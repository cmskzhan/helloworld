import logging
from mega import Mega
import os

class MegaNZClient:
    """
    A reusable client for interacting with MEGA.nz storage.
    """
    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password
        self.mega = Mega()
        self.m = None

    def login(self, email=None, password=None):
        """
        Logs into MEGA. Email and password can be provided here or in __init__.
        """
        if email:
            self.email = email
        if password:
            self.password = password
            
        if not self.email or not self.password:
            raise ValueError("Email and password are required for login.")

        logging.info(f"Logging into MEGA as {self.email}...")
        try:
            self.m = self.mega.login(self.email, self.password)
            logging.info("Successfully logged in!")
            return self.m
        except Exception as e:
            logging.error(f"Login failed: {e}")
            raise

    def list_files(self):
        """
        Lists files currently in the MEGA account.
        """
        if not self.m:
            raise Exception("Please login first by calling login().")
            
        logging.info("--- Your MEGA Files ---")
        files = self.m.get_files()
        for file_id, file_info in files.items():
            # Extract filename from metadata 'a' -> 'n'
            file_name = file_info.get("a", {}).get("n")
            is_folder = file_info.get("t") == 1
            if file_name:
                suffix = "/" if is_folder else ""
                logging.info(f"- {file_name}{suffix} (ID: {file_id})")
        logging.info("-----------------------\n")

    def upload(self, local_file_path, destination_folder_name=None):
        """
        Uploads a local file to MEGA.
        """
        if not self.m:
            raise Exception("Please login first by calling login().")
            
        handle = None
        if destination_folder_name:
            # If the user passed a handle directly (8 chars usually), try it
            # But mostly they pass names. Resolve name to handle.
            node = self.m.find(destination_folder_name)
            if node and isinstance(node, tuple):
                handle = node[0]
            else:
                # Check if it might be a handle already (though risky to guess)
                # If m.get_node(destination_folder_name) works, then it's a handle
                try:
                    # Just in case they passed a handle
                    if self.m.get_node(destination_folder_name):
                        handle = destination_folder_name
                except:
                    pass
                
                if not handle:
                    logging.warning(f"Warning: Folder '{destination_folder_name}' not found. Uploading to root.")
        
        target_dest = destination_folder_name if handle else "root"
        logging.info(f"Uploading '{local_file_path}' to {target_dest} on MEGA {self.email} account...")
        try:
            uploaded_file = self.m.upload(local_file_path, handle)
            logging.info("Upload complete!")
            return uploaded_file
        except Exception as e:
            logging.error(f"Upload failed: {e}")
            raise

    def download(self, filename, dest_path=None):
        """
        Downloads a file from MEGA by its name.
        """
        if not self.m:
            raise Exception("Please login first by calling login().")
            
        logging.info(f"Attempting to download '{filename}' from MEGA...")
        try:
            # find_by_name returns the file node if found, or None
            file_node = self.m.find(filename)
            if file_node:
                downloaded_path = self.m.download(file_node, dest_path)
                logging.info(f"Download complete! Saved to: {downloaded_path}")
                return downloaded_path
            else:
                logging.error(f"File '{filename}' not found in your MEGA storage.")
                return None
        except Exception as e:
            logging.error(f"Download failed: {e}")
            raise

    def troubleshoot(self):
        """
        Runs detailed troubleshooting logic for login issues.
        """
        logging.basicConfig(level=logging.DEBUG)
        logging.info(f"--- Starting Troubleshooting for {self.email} ---")
        try:
            self.login()
            logging.info("Login Successful!")
        except Exception as e:
            logging.error("\n--- ERROR ANALYSIS ---")
            logging.error(f"Error Type: {type(e).__name__}")
            logging.error(f"Error Message: {e}")
            logging.error("\nPossible Causes:")
            logging.error("1. IP Block: MEGA may be blocking your current network.")
            logging.error("2. 2FA: Two-Factor Authentication may be enabled.")
            logging.error("3. Maintenance: The MEGA API endpoint may be temporarily down.")
            if "Expecting value" in str(e):
                logging.error("\nTechnical Detail: The server sent a non-JSON response. Check DEBUG logs.")

if __name__ == "__main__":
    email = os.getenv("MEGA_YAHOO_USERNAME")
    password = os.getenv("MEGA_YAHOO_PASSWORD")
    
    if email and password:
        client = MegaNZClient(email, password)
        try:
            client.login()
            client.list_files()
            # Ensure the path is correct if run from root
            path = "requirements.txt" if os.path.exists("requirements.txt") else None
            if not path:
                raise FileNotFoundError("requirements.txt not found in project root.")
            client.upload(path, "news")
            # client.download("test.txt")
        except Exception as e:
            client.troubleshoot()
    else:
        print("Usage: Set MEGA_YAHOO_USERNAME and MEGA_YAHOO_PASSWORD to run example.")
