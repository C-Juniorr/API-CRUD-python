import flet as ft
import requests

def main(page:ft.Page):
    page.clean()
    def vertudo():
        response = requests.get("http://127.0.0.1:5000/usuarios")
        if response.status_code == 200:
            page.clean()
            usuariosdata = response.json()
            print(usuariosdata)
            for usuario in usuariosdata:
                page.add(
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(f"ID: {usuario["id"]}", color="black", bgcolor="yellow", size=22),
                                ft.Text(f"ID: {usuario["name"]}", color="black", bgcolor="yellow", size=22),
                                ft.Text(f"ID: {usuario["email"]}", color="black", bgcolor="yellow", size=22)
                            ]
                        )
                    )
                )
            page.add(ft.ElevatedButton("Voltar", on_click= lambda e: main(page)))

    def verbyemail():

        def puxarviaemail(email):
            if email:
                page.clean()
                response = requests.get(f"http://127.0.0.1:5000/usuarios/{email}")
                print(response)
                if response.status_code == 200 or response.status_code == 201:
                    dados = response.json()
                    page.add(ft.Container(
                        ft.Column(
                            [
                                ft.Text(f"id: {dados["id"]}", color="yellow", bgcolor="black"),
                                ft.Text(f"id: {dados["name"]}", color="yellow", bgcolor="black"),
                                ft.Text(f"id: {dados["email"]}", color="yellow", bgcolor="black")
                            ]
                        )
                    ))
                page.add(ft.ElevatedButton("Voltar", on_click= lambda e: main(page)))

            else:
                snack_bar = ft.SnackBar(ft.Text("DIGITE UM VALOR VALIDO: ", color="red"))
                snack_bar.open = True
                page.snack_bar = snack_bar
                page.update()

        page.clean()
        lblemail = ft.TextField(label="DIGITE O EMAIL DO USUARIO: ")
        btnenviar = ft.ElevatedButton("ENVIAR", on_click=lambda e: puxarviaemail(lblemail.value))
        page.add(ft.Container(
            ft.Column(
                [
                    lblemail,
                    btnenviar
                ]
            )
        )),

    def adduser():
        def enviar():
            if lblname.value and lblemail.value and lblsenha.value:
                user = {"name": lblname.value, "email": lblemail.value, "password": lblsenha.value}
                response = requests.post("http://127.0.0.1:5000/usuarios", json=user)
                if response.status_code == 201:
                    rps = response.json()
                    snack_bar = ft.SnackBar(ft.Text(rps, color="green"))
                    snack_bar.open = True
                    page.snack_bar = snack_bar
                    page.update()
                elif response.status_code == 409:
                    rps = response.json()
                    snack_bar = ft.SnackBar(ft.Text(rps, color="red"))
                    snack_bar.open = True
                    page.snack_bar = snack_bar
                    page.update()


        page.clean()
        lblname = ft.TextField(label="SEU NOME:")
        lblemail = ft.TextField(label="Seu Email: ")
        lblsenha = ft.TextField(label="Sua Senha: ")
        btnenviar = ft.ElevatedButton("Registrar", on_click=lambda e: enviar())
        page.add(
            ft.Container(
                ft.Column(
                    [
                        lblname,
                        lblemail,
                        lblsenha,
                        btnenviar
                    ],
                    alignment="center"
                ),
                alignment=ft.alignment.center
            )#Adolfo@gmail.com
        ),
        page.add(ft.ElevatedButton("Voltar", on_click= lambda e: main(page)))
    
    def attuser():
        def attbbtn():
            if txtnm.value and txtemail.value and txtpwd:
                user = {"name": txtnm.value, "email": txtemail.value, "password": txtpwd.value}
                response = requests.put(f"http://127.0.0.1:5000/usuarios/{txtid.value}", json=user)
                if response.status_code == 200:
                    rps = response.json()
                    snack_bar = ft.SnackBar(ft.Text(rps, color="green"))
                    snack_bar.open = True
                    page.snack_bar = snack_bar
                    page.update()
                else:
                    rps = response.json()
                    snack_bar = ft.SnackBar(ft.Text(rps, color="red"))
                    snack_bar.open = True
                    page.snack_bar = snack_bar
                    page.update()
                    

        page.clean()
        txtid = ft.TextField(label="ID DO USUARIO QUE SER EDITADO: ")
        txtnm = ft.TextField(label="NOVO NOME: ")
        txtemail = ft.TextField(label="NOVO EMAIL: ")
        txtpwd = ft.TextField(label="NOVA SENHA: ")
        btnenv = ft.ElevatedButton("ATUALIZAR", on_click=lambda e: attbbtn())
        page.add(ft.Container(
            ft.Column(
                [
                    txtid,
                    txtnm,
                    txtemail,
                    txtpwd,
                    btnenv
                ],
                alignment="center"
            ),
            alignment=ft.alignment.center
        )),
        page.add(ft.ElevatedButton("Voltar", on_click= lambda e: main(page)))

    def dltuser():
        def excluiruser():
            if txtid.value:
                response = requests.delete(f"http://127.0.0.1:5000/usuarios/{txtid.value}")
                if response.status_code == 200 or response.status_code == 201:
                    rps = response.json()
                    snack_bar = ft.SnackBar(ft.Text(rps, color="green"))
                    snack_bar.open = True
                    page.snack_bar = snack_bar
                    page.update()
                else:
                    rps = response.json()
                    snack_bar = ft.SnackBar(ft.Text(rps, color="red"))
                    snack_bar.open = True
                    page.snack_bar = snack_bar
                    page.update()


        page.clean()
        txtid = ft.TextField(label="Id do usuario para excluir: ")
        btnexcluir = ft.ElevatedButton("Excluir", on_click=lambda e: excluiruser())
        page.add(ft.Container(
            ft.Column(
                [
                    txtid,
                    btnexcluir

                ]
            )
        ))
        page.add(ft.ElevatedButton("Voltar", on_click= lambda e: main(page)))
    
    def lgnuser():
        def logaruser():
            if txtemail.value and txtsenha.value:
                userlgn = {"email": txtemail.value, "password": txtsenha.value}
                response = requests.post("http://127.0.0.1:5000/login", json=userlgn)
                if response.status_code == 200:
                    page.clean()
                    rps = response.json()
                    snack_bar = ft.SnackBar(ft.Text(f'USUARIO LOGADO COM SUCESSO\n{rps}', color="green"))
                    snack_bar.open = True
                    page.snack_bar = snack_bar
                    page.update()
                    dados = response.json()
                    userid = dados["id"]
                    userem = dados["email"]
                    txtid = ft.Text(userid, color="green", size=24, bgcolor="black", weight="bold")
                    txtnm = ft.Text(userem, color="green", size=25, bgcolor="black", weight="bold")
                    page.add(ft.Container(
                        ft.Row(
                            [
                                txtid,
                                txtnm
                            ],
                            alignment="center"
                        ),
                        alignment=ft.alignment.center
                    ))

                elif response.status_code == 400:
                    rps = response.json()
                    snack_bar = ft.SnackBar(ft.Text(rps, color="red"))
                    snack_bar.open = True
                    page.snack_bar = snack_bar
                    page.update()
        page.clean()
        txtemail = ft.TextField(label="Email: ")
        txtsenha = ft.TextField(label="Senha: ")
        btnlgn = ft.ElevatedButton("LOGIN", on_click=lambda e: logaruser())
        page.add(ft.Container(
            ft.Column(
                [
                    txtemail,
                    txtsenha,
                    btnlgn
                ],
                alignment="center"
            ),
            alignment=ft.alignment.center
        ))
    
    btnver = ft.ElevatedButton("VER TODOS OS USUARIOS", on_click=lambda e: vertudo())
    btnver1 = ft.ElevatedButton("VER UM USUARIO PELO EMAIL", on_click=lambda e: verbyemail())
    btnadd = ft.ElevatedButton("ADICIONAR USUARIO", on_click=lambda e: adduser())
    btnatt = ft.ElevatedButton("ATUALIZAR DADOS DO USUARIO", on_click=lambda e: attuser())
    btndlt = ft.ElevatedButton("DELETAR USUARIO", on_click=lambda e: dltuser())
    btnlgn = ft.ElevatedButton("LOGIN DE USUARIO", on_click=lambda e: lgnuser())
    ttl = ft.Text("APLICAÇÃO PARA TESTAR API INTEGRADA COM DB", color="green", size=30, weight="bold")
    ttl2 = ft.Text("Producted by: CLODOALDO JUNIOR", color="black", size=20, weight="bold")
    page.add(
        ft.Container(
            ft.Column(
                [
                    ttl,
                    ttl2
                ],
                alignment="center"
                ),
                alignment=ft.alignment.center
            ),

        ft.Container(
            ft.Column(
                [
                    btnver,
                    btnver1,
                    btnadd,
                    btnatt,
                    btndlt,
                    btnlgn
                ],
                alignment=ft.alignment.center,
                horizontal_alignment=ft.alignment.center
            ),
            alignment=ft.alignment.center
        )
    )

ft.app(main)