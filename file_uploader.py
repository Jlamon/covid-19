import pandas as pd
import dash_html_components as html
import base64
import io


def file_uploader(file_content, filename):
    if file_content is not None:
        content_type, content_string = file_content.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                df = pd.read_csv(io.StringIO(decoded.decode()))
                df.columns = df.columns.str.replace(' ', '')
                df.to_csv('data/user_input.csv', index=False)

        except Exception as e:
            print(e)
            return html.Div(['There was an Error.'])

        return html.Div(['The file has been uploaded'])
