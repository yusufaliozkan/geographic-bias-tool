import streamlit.components.v1 as components
import datetime
import streamlit as st

current_year = datetime.datetime.now().year  
cite_today = datetime.date.today().strftime("%d %B %Y")

def display_custom_license():
    components.html(
    f"""
    <br><a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" 
    src="https://i.creativecommons.org/l/by/4.0/80x15.png" /></a><br />
    © {current_year} Imperial College London. All rights reserved. This tool is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
    </br>
    <br>
    <strong>Cite this page:</strong> Imperial College London ‘<em>Geographic Bias Tool</em>’, Created July 2024, Accessed {cite_today}. <a href="https://geographic-bias-tool.streamlit.app/">https://geographic-bias-tool.streamlit.app/</a>.
    </br>
    """
    )

def cc_by_licence_image():
    components.html(
    f"""
    <br><a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" 
    src="https://i.creativecommons.org/l/by/4.0/80x15.png" /></a><br />
    © {current_year} Imperial College London. All rights reserved. This tool is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
    </br>
    <br>
    """
    )