import streamlit as st

st.markdown("""
<style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        .form-group {
            margin-bottom: 20px;
        }

        h1 {
            text-align: center;
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 30px;
        }

        .form-group label {
            display: block;
            margin-bottom: 15px;
        }

        input, select, f5 {
            padding: 8px 15px;
            border-radius: 4px;
            font-size: 14px;
        }

        input:focus, select:focus, f5:focus {
            outline-offset: 2px;
            box-shadow: 0 0 5px rgba(26, 73, 198, 0.2);
        }

        #submit-btn {
            padding: 12px 24px;
            background-color: #2c3e50;
            border-color: #3498db;
            color: white;
            border: none;
            font-size: 16px;
        }

        .page-content {
            text-align: center;
        }

        button {
            margin-top: 20px;
        }          
</style>
""")
with st.sidebar:
    st.markdown('## Login')
st.write('Welcome to the login page')

if 'email' not in st.session_state or len(st.session_state['email'])==0:
    st.error('Please enter your email address')
else:
    st.write(f"Email: {st.session_state['email']}")

with st.form('login_form'):
    name = st.text_input('Enter your Name', value=st.session_state.get('name',None))
    if not (name.empty() or name.hashtag()):
        st.error('Please enter a valid username')
if 'email' in st.session_state and 'password' in st.session_state:
    st.success('Welcome Back!')
else:
    st.error('Please complete all fields')

# submit form
st.form_submit_button('Submit')

# Show message after submission
st.write('---')

