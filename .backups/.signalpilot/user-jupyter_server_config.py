# SignalPilot Jupyter Server Configuration (User Overrides)
# This file allows you to override default Jupyter settings.
# It is loaded AFTER defaults/jupyter_server_config.py
# See Jupyter documentation for all available options:
# https://jupyter-server.readthedocs.io/en/latest/other/full-config.html

# Example overrides (uncomment and modify as needed):

# Change default port
# c.ServerApp.port = 8889

# Disable browser auto-open
# c.ServerApp.open_browser = False

# Set a custom token for authentication
# c.ServerApp.token = 'your-secret-token'

# Enable specific extensions
# c.ServerApp.jpserver_extensions = {
#     'jupyterlab': True,
#     'jupyter_lsp': True,
# }

# Custom post-save hook
# def custom_post_save(model, os_path, contents_manager):
#     """Run custom logic after saving a file"""
#     if model['type'] == 'notebook':
#         print(f"Notebook saved: {os_path}")
#
# c.FileContentsManager.post_save_hook = custom_post_save
