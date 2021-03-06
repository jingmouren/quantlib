import json
from html import escape
from contextlib import contextmanager
# from itertools import starmap
import pandas as pd


class Tag:
    """HTML tag"""
    def __init__(self, _name, parent=None, _content=None, _inline=False, **kwargs):
        self.name = _name
        self.parent = parent
        if "_class" in kwargs:
            kwargs["class"] = kwargs["_class"]
            del kwargs["_class"]
        self.attrs = kwargs
        self.inline = _inline
        self.content = _content or []

    def prepend(self, item):
        """prepend an element"""
        self.content.insert(0, item)

    def append(self, item):
        """Append an element"""
        self.content.append(item)

    def render(self):
        """Show HTML code
        Returns
        -------
        List[str]
            each element is a line
        """
        # attrs = ' '.join(starmap(lambda key, value: '%s="%s"' % (key, value), self.attrs.items()))
        attrs = []
        for key, value in self.attrs.items():
            if isinstance(value, (list, tuple)):
                value = " ".join(value)
            attrs.append('%s="%s"' % (key, value))
        attrs = ' '.join(attrs)
        if attrs:
            tag_open = '<%s %s>' % (self.name, attrs)
        else:
            tag_open = '<%s>' % self.name
        tag_close = '</%s>' % self.name
        if self.inline:
            html = ["  {open}{content}{close}".format(
                open=tag_open,
                content="".join("".join(c.render()) for c in self.content),
                close=tag_close
            )]
        else:
            html = []
            html.append(tag_open)
            for doc in self.content:
                html += doc.render()
            html.append(tag_close)
            html = ["  " + line for line in html]
        return html


class Text(Tag):
    """An element that contains only pure text"""
    def __init__(self, text, parent=None):
        self.text = escape(text)
        self.parent = parent

    def render(self):
        return [self.text]


class Tab(Tag):
    def __init__(self, parent=None):
        self.parent = parent
        self.menu = Tag("ul", parent=self, _class=["nav", "nav-tabs"])
        self.tabs = []
        self.content = {}
    
    def add_tab(self, tab_name, text):
        if tab_name in self.tabs:
            import warnings
            warnings.warn("Tab `{name}` already exists".format(name=tab_name))
        self.tabs.append(tab_name)
        _class = ["tab-pane", "fade"]
        default = len(self.tabs) == 1
        if default:
            _class.extend(["active", "in"])
        self.content[tab_name] = Tag("div", parent=self, _class=_class, id=tab_name)
        self.menu.append(Tag("li", _class="active" if default else "",
                             _content=[Tag("a", href="#%s" % tab_name, _content=[Text(text)], **{'data-toggle': 'tab'})]))
        return self.content[tab_name]

    def __getitem__(self, key):
        return self.content[key]

    def render(self):
        menu_render = self.menu.render()
        div = Tag("div", _class="tab-content", _content=[self.content[key] for key in self.tabs])
        content_render = div.render()
        return menu_render + content_render


class RawHtml(Tag):
    """An element that contains raw html"""
    def __init__(self, html, parent=None):
        self.text = html
        self.parent = parent

    def render(self):
        return [self.text]


class HTMLBase:
    """用上下文管理器生成HTML文档

    Example
    -------
    ..  code-block:: python

        doc = HTML()
        with doc.html():
            with doc.head():
                doc.inline("titile", _text="Generated HTML")
            with doc.body():
                with doc.div(_class="container"):
                    with doc.div(_class="row"):
                        doc.inline("p", _text="paragraph")
        html = doc.render()
    """
    def __init__(self):
        self.root = Tag("html")
        self.head = Tag("head")
        self.body = Tag("body")
        self.root.append(self.head)
        self.root.append(self.body)
        self.__main = [self.root]

    def append(self, node):
        """Append an element"""
        self.__main.append(node)

    @property
    def main(self):
        """The current main element"""
        return self.__main[-1]

    def __getattr__(self, tag_name):
        @contextmanager
        def wrapped(**kwargs):
            node = Tag(tag_name, parent=self.main, **kwargs)
            self.main.append(node)
            self.__main.append(node)
            yield node
            self.__main.pop()
        return wrapped

    def text(self, text):
        node = Text(text)
        self.main.append(node)

    def html(self, html):
        self.main.append(RawHtml(html))

    def inline(self, tag_name, _text=None, **kwargs):
        content = [Text(_text)] if _text else None
        node = Tag(tag_name, **kwargs, _inline=True, _content=content)
        self.main.append(node)

    def render(self, file_path=None):
        html = "\n".join(self.root.render())
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
        return html

    @contextmanager
    def use(self, node):
        self.__main.append(node)
        yield node
        self.__main.pop()


class HTML(HTMLBase):
    def __init__(self, enable_highcharts=False, enable_bootstrap=True, enable_mathjax=False):
        super(HTML, self).__init__()
        with self.use(self.head):
            if enable_bootstrap:
                self.inline("meta", charset="utf-8")
                self.inline("meta", name="viewport", content="width=device-width, initial-scale=1")
                self.inline("link", rel="stylesheet", href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css", type="text/css")
                # self.inline("link", rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", type="text/css")
                # self.inline("link", rel="stylesheet", href="https://pingendo.github.io/templates/blank/theme.css", type="text/css")
            if enable_mathjax:
                with self.script(type="text/x-mathjax-config"):
                    self.html("MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});")
                # self.inline("script", src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js", type="text/javascript")
                self.inline("script", src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML", type="text/javascript")
        with self.use(self.body):
            if enable_highcharts:
                self.inline("script", src="https://code.highcharts.com/highcharts.js")
                # self.inline("script", src="https://code.highcharts.com/stock/highstock.js")
                self.inline("script", src="https://code.highcharts.com/stock/modules/exporting.js")
            if enable_bootstrap:
                self.inline("script", src="https://code.jquery.com/jquery-3.1.1.min.js")
                # self.inline("script", src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js")
                self.inline("script", src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js")

    def container(self):
        node = Tag("div", _class="container", parent=self.body)
        self.body.append(node)
        return node

    def row(self, container):
        node = Tag("div", _class="row", parent=container)
        container.append(node)
        return node

    def col(self, row, width=12):
        if not isinstance(width, (list, tuple)):
            width = (width, )
        nodes = []
        for w in width:
            node = Tag("div", _class="col-md-%d" % w)
            nodes.append(node)
            row.append(node)
        if len(nodes) > 1:
            return nodes
        else:
            return node

    def highcharts(self, name, data, plot_type=None, options=None, **kwargs):
        """
        Insert highcharts.

        Parameters
        ----------
        name: str
            Name of the chart.
        data: pd.DataFrame
            data to be converted to chart
        plot_type: dict
            type to be plotted
        options: dict
            other options to pass to highcharts
        """
        plot_type = plot_type or {}
        if isinstance(plot_type, str):
            if isinstance(data, pd.DataFrame):
                plot_type = {col_name: plot_type for col_name in data.columns}
            else:
                plot_type = {data.name: plot_type}
        self.inline('div', id="highcharts-%s" % name.replace(" ", ""), **kwargs)
        embedded_data = []
        if isinstance(data, pd.DataFrame):
            for col in data.columns:
                series = data[col]
                embedded_data.append((series.name, self.series2json(series)))
        elif isinstance(data, pd.Series):
            embedded_data.append((data.name, self.series2json(data)))
        else:
            raise TypeError("Data must be either DataFrame or Series")

        highcharts_data = {
            'title': {
                'text': name
            },
            'series': [
                {
                    'name': s_name,
                    'data': s_value,
                    'type': plot_type.get(s_name, "line"),
                    'tooltip': {
                        'valueDecimals': 3
                    }
                }
                for s_name, s_value in embedded_data
            ]
        }
        if options:
            highcharts_data.update(options)

        if isinstance(data.index, pd.DatetimeIndex):
            highcharts_data['xAxis'] = {'type': 'datetime'}
        elif isinstance(data.index, pd.CategoricalIndex) or data.index.dtype.name == "object":
            highcharts_data['xAxis'] = {'type': 'category'}
        else:
            highcharts_data['xAxis'] = {'type': 'linear'}

        js_code = "Highcharts.chart('highcharts-{name}', {data});".format(name=name, data=json.dumps(highcharts_data, indent=2, sort_keys=True))

        with self.script():
            self.html(js_code)

    @staticmethod
    def series2json(series):
        """把pd.Series时间序列转换为json格式"""
        series = series.copy().dropna()
        if isinstance(series.index, pd.DatetimeIndex):
            series.index = series.index.astype(int) / 1e6
        return sorted([[int(key), float(value)] for key, value in series.to_dict().items()])

    def generate_table(self, data,
                       caption=None,
                       show_headers=True,
                       show_index=True,
                       hover=True,
                       bordered=True,
                       striped=False,
                       condensed=False,
                       format="{:.2f}",
                       **kwargs):
        """Generate a table

        Parameters
        ----------
        data: pd.DataFrame
            data to be converted to a table
        caption: str
            caption to show, optional
        show_headers: bool, optional
            whether to show the column names as first row
        show_index: bool, optional
            whether to show the index as first column
        hover: bool, optional
            table-hover class
        bordered: bool, optional
            table-bordered class
        striped: bool, optional
            table-striped class
        condensed: bool, optional
            table-condensed class
        format: str, optional
            the format to show the values
        kwargs
            other attributes to be added to table

        See Also
        --------
        pd.DataFrame.style: Another way to generate beautiful html table from pd.DataFrame
        """
        if "_class" in kwargs:
            kwargs["_class"].append("table")
        else:
            kwargs["_class"] = ["table"]
        if hover:
            kwargs["_class"].append("table-hover")
        if bordered:
            kwargs["_class"].append("table-bordered")
        if striped:
            kwargs["_class"].append("table-striped")
        if condensed:
            kwargs["_class"].append("table-condensed")
        with self.table(**kwargs):
            if caption:
                self.inline("caption", _text=caption)
            if show_headers:
                with self.thead():
                    with self.tr():
                        if show_index:
                            self.inline('th', _text=data.index.name or "#")
                        for col in data.columns:
                            self.inline("th", _text=col)
            with self.tbody():
                for idx, data in data.iterrows():
                    with self.tr():
                        if show_index:
                            self.inline("td", _text=str(idx))
                        for val in data:
                            self.inline('td', _text=format.format(val))

    def tab(self):
        tag = Tab(parent=self.main)
        self.main.append(tag)
        return tag
