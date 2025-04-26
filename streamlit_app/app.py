import streamlit as st
import yaml, subprocess

st.title("Autoloader Configurator")

# 1. Form inputs
source = st.text_input("Source Path")
target = st.text_input("Target Path")
fmt    = st.selectbox("Format", ["csv","json","excel"])
infer  = st.checkbox("Infer Schema?", True)
mode   = st.radio("Ingestion Mode", ["create","append","overwrite"])
layer  = st.selectbox("Layer", ["bronze","silver","gold"])
part   = st.text_input("Partition Column (optional)")

if st.button("Generate & Deploy"):
    cfg = {
      "pipeline_name": f"{layer}_poc",
      "source_path": source,
      "target_path": target,
      "format": fmt,
      "schema_infer": infer,
      "explicit_schema": [],
      "layer": layer,
      "ingest_mode": mode,
      "partition_column": part or None
    }
    repo_owner = "supriya.chikkam@cxdatalabs.com"
    repo_name  = "cxdl-utimco-repo"
    path       = "streamlit_app/test1.txt"
    url        = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    
    data = {
      "message": f"Add {layer}_poc pipeline",
      #"content": encoded,
      "branch": "main",           # optional, defaults to default branch
      "sha":     "<old-sha-if-updating>"
    }

    # 4) call
    headers = {"Authorization": f"token {st.secrets['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']}"}
    r = requests.put(url, json=data, headers=headers)

    if r.status_code in (200, 201):
        st.success("✅ test1.txt created in GitHub!")
    else:
        st.error(f"GitHub API error {r.status_code}: {r.json()}")
    
    # with open("test1.txt", "w") as f:
    #     f.write("This is a test file.")
    # subprocess.run(["git","add","streamlit_app/test1.txt"])
    # subprocess.run(["git","commit","-m","streamlit_app/test1.txt"])
    # subprocess.run(["git","push"])


    # with open("dash-hello-world-app/configs/bronze_poc.yaml", "w") as f:
    #     yaml.dump(cfg, f)
    # 2. Commit & push to Git
    # subprocess.run(["git","add","configs/*.yaml"])
    # subprocess.run(["git","add","test1.txt"])
    # subprocess.run(["git","commit","-m",f"Add {layer}_poc pipeline"])
    # subprocess.run(["git","push"])
    # 3. Trigger Databricks job run via CLI
    # subprocess.run([
    #   "databricks","jobs","run-now",
    #   "--job-id","<JOB_ID>",
    #   "--notebook-params",
    #   f'{{"config_path":"configs/{layer}_poc.yaml"}}'
    #])
    st.success("Pipeline config created and job triggered!")
