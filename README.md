# jh-save

A JupyterHub service that provides a URL endpoint for logged-in users to save a compressed archive of all of their files on the server. 
Authentication is handled by JupyterHub. To use, navigate to
```
{jupyterhub base url}/services/jh-save
```

To install, ensure `jh-save` is a listed service in your `jupyterhub_config.py`, and that `JUPYTERHUB_USER_PATH` is set properly. To configure what files are included in the archive, set the `JUPYTERHUB_SAVE_REGEX` accordingly.