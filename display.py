import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import re

node_size_inflater = 10


# g.add_node(territory, label=label, fontsize=30,
#            pos=territory.board_pos, fixedsize=True,
#            height=territory.size_on_board, width=territory.size_on_board,
#            shape='oval', fontcolor='#FFFFFF', penwidth=35,
#            fillcolor=territory.fill_color, color=territory.border_color,
#            style='filled')


class Display:
    def __init__(self):
        self.graphs = []
        self.app = dash.Dash(__name__)
        self.names = []

    def add_graph(self, graph, name):
        self.graphs.append(graph)
        new_trace = self.make_trace_from_graph(graph)
        if len(self.graphs) != 1:
            self.fig.add_trace(new_trace)
        self.names.append(name)

    def make_first_display(self, g):
        """
        creates elements of the display that will not change if more graphs are added.
        :param g:
        :return:
        """
        p = re.compile(r'(?P<x>[\d\.]+),(?P<y>[\d\.]+)!')
        self.node_x = []
        self.node_y = []
        self.node_number = dict()
        for i, node in enumerate(g.nodes()):
            m = p.search(g.nodes[node]['pos'])
            if not m:
                raise Exception(f'couldnt read node position {g.nodes[node]["pos"]} !!!!!')
            self.node_x.append(float(m.group("x")))
            self.node_y.append(float(m.group("y")))
            self.node_number[node] = i

        self.sizes = [node_size_inflater * float(territory.size_on_board) for territory in
                      g.nodes()]
        # self.colors = ["blue"] * len(g.nodes())
        colors = [territory.fill_color for territory in g.nodes()]
        texts = [f'{territory.name} <br> {territory.troops}<br>' for
                 territory in g.nodes()]
        self.border_colors = [territory.border_color for territory in g.nodes()]
        node_trace = go.Scatter(x=self.node_x, y=self.node_y, mode='markers+text',
                                hovertemplate="%{text}", textfont_size=14, text=texts,
                                marker=dict(color=colors, size=self.sizes, line_width=10,
                                            line_color=self.border_colors), )

        self.edge_x = []
        self.edge_y = []
        for node1, node2 in g.edges():
            n1, n2 = self.node_number[node1], self.node_number[node2]
            self.edge_x += [self.node_x[n1], self.node_x[n2], None]
            self.edge_y += [self.node_y[n1], self.node_y[n2], None]

        self.edge_trace = go.Scatter(x=self.edge_x, y=self.edge_y,
                                     line=dict(width=0.5, color='#888'),
                                     hoverinfo='none', mode='lines')

        self.layout = go.Layout(showlegend=False, hovermode='closest',
                                margin=dict(b=5, l=5, r=5, t=0), height=500,
                                xaxis=dict(visible=False, showgrid=False, showline=False),
                                yaxis=dict(visible=False, showgrid=False))
        self.graph_name = "risky_graph"
        self.fig = go.Figure(data=[self.edge_trace, node_trace],
                             layout=self.layout)
        return node_trace

    def make_trace_from_graph(self, g):
        if len(self.graphs) == 1:
            return self.make_first_display(g)
        colors = [territory.fill_color for territory in g.nodes()]
        texts = [f'{territory.name} <br> {territory.troops}<br>' for
                 territory in g.nodes()]
        node_trace = go.Scatter(visible=False, x=self.node_x, y=self.node_y, mode='markers+text',
                                hovertemplate="%{text}", textfont_size=14, text=texts,
                                marker=dict(color=colors, size=self.sizes, line_width=10,
                                            line_color=self.border_colors), )
        return node_trace

    def create_slider(self):
        steps = []
        for i in range(1, len(self.fig.data)):
            step = dict(
                method="update",
                args=[{"visible": [True] + [False] * (len(self.fig.data) - 1)},
                      {"title": "Slider switched to step: " + str(i)}],  # layout attribute
                label=self.names[i-1],
            )
            step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
            steps.append(step)

        sliders = [dict(
            active=10,
            # currentvalue={"prefix": "Frequency: "},
            # pad={"t": 50},
            steps=steps,
        )]

        self.fig.update_layout(sliders=sliders)

    def disp(self):
        if not self.graphs:
            print("no graph to display")
            return
        self.create_slider()
        self.app.layout = html.Div(children=[
            html.H1(children='Risk'),
            html.H3(children="Color indicates the current territory owner."),
            html.H3(children="Border color indicates the continent."),
            dcc.Graph(id=self.graph_name, figure=self.fig, ),
        ])
        self.app.run_server(debug=False)
        # self.app.run_server(debug=True)
