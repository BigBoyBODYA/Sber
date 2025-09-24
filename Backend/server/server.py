from gigachat import GigaChat
import ssl

ssl_context = ssl.create_default_context()


giga = GigaChat(
   credentials="MDE5OTc1YzktMTIxZS03NTM1LWEzNDYtNTUyY2Y4ZTMzYzg2OjM1NTYzYmRhLTk1N2EtNDYwZC04YjkyLTUxZTUwNjY0YWI0Yg==",
   ssl_context=False,
   ca_bundle_file="russian_trusted_root_ca.cer"
)

response = giga.get_token()

print(response.access_token)

request = input("Запрос:")
response = giga.chat(request)
print(response.choices[0].message.content)