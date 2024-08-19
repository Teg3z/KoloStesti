from dotenv import load_dotenv
import os
import sys

# Load environment variables from .env file
load_dotenv(dotenv_path='variables.env')

def get_env_var_value(env_var_name):
    env_var_value = os.getenv(env_var_name)
    if env_var_value is None:
        print(f"Environment variable {env_var_name} weren't loaded correctly. Exiting...")
        sys.exit(1)  # Exit with a non-zero status code to indicate an error
    return env_var_value

def main():
  get_env_var_value("DISCORD_BOT_TOKEN")

if __name__ == '__main__':
    main()
