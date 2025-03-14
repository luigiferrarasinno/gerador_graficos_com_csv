import gradio as gr
import plotly.express as px
import pandas as pd

# Função para gerar o gráfico
def plot_graph(chart_type, file, x_col, y_col):
    try:
        df = pd.read_csv(file.name)
        
        if x_col not in df.columns or y_col not in df.columns:
            return px.scatter(title="Erro: Selecione colunas válidas para X e Y.")
        
        if chart_type == "Linha":
            fig = px.line(df, x=x_col, y=y_col, title="Gráfico de Linha")
        elif chart_type == "Barra":
            fig = px.bar(df, x=x_col, y=y_col, title="Gráfico de Barra")
        elif chart_type == "Dispersão":
            fig = px.scatter(df, x=x_col, y=y_col, title="Gráfico de Dispersão")
        elif chart_type == "Pizza":
            fig = px.pie(df, names=x_col, values=y_col, title="Gráfico de Pizza")
        else:
            fig = px.scatter(title="Escolha um tipo de gráfico válido.")
        
        return fig
    except Exception as e:
        return px.scatter(title=f"Erro ao processar o arquivo: {e}")

# Função para atualizar colunas disponíveis após upload do CSV
def update_columns(file):
    try:
        df = pd.read_csv(file.name)
        colunas = list(df.columns)
        return gr.Dropdown(choices=colunas, value=colunas[0] if colunas else None), gr.Dropdown(choices=colunas, value=colunas[1] if len(colunas) > 1 else None)
    except:
        return gr.Dropdown(choices=[], value=None), gr.Dropdown(choices=[], value=None)

# Interface Gradio
with gr.Blocks() as app:
    gr.Markdown("# 📊 Criador de Gráficos Avançado")
    gr.Markdown("Faça upload de um arquivo CSV, selecione as colunas e visualize seus dados.")

    chart_type = gr.Radio(["Linha", "Barra", "Dispersão", "Pizza"], label="Escolha o tipo de gráfico")
    file_input = gr.File(label="Faça upload do seu arquivo CSV")
    x_column = gr.Dropdown(choices=[], label="Selecione a coluna X")
    y_column = gr.Dropdown(choices=[], label="Selecione a coluna Y")
    graph_output = gr.Plot()
    btn = gr.Button("Gerar Gráfico")
    
    file_input.change(update_columns, inputs=[file_input], outputs=[x_column, y_column])
    btn.click(plot_graph, inputs=[chart_type, file_input, x_column, y_column], outputs=graph_output)

app.launch()