<!DOCTYPE html>
<html lang="en">
<head>
    <!--[if lt IE 9]>
    <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Serialization demo</title>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="../dist/gridstack.css"/>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.11.0/jquery-ui.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/3.5.0/lodash.min.js"></script>
    <script src="../dist/gridstack.js"></script>
    <script src="../dist/gridstack.jQueryUI.js"></script>

    <style type="text/css">
        .grid-stack {
            background: lightgoldenrodyellow;
        }

        .grid-stack-item-content {
            color: #2c3e50;
            text-align: center;
            background-color: #18bc9c;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <h1>Serialization demo</h1>

        <div>
            <a class="btn btn-default" id="save-grid" href="#">Save Grid</a>
            <a class="btn btn-default" id="load-grid" href="#">Load Grid</a>
            <a class="btn btn-default" id="clear-grid" href="#">Clear Grid</a>
        </div>

        <br/>

        <div class="grid-stack">
        </div>

        <hr/>

        <textarea id="saved-data" cols="100" rows="20" readonly="readonly"></textarea>
    </div>


    <script type="text/javascript">
        $(function () {
            var options = {
            };
            $('.grid-stack').gridstack(options);

            new function () {
                this.serializedData = [
                    {x: 0, y: 0, width: 2, height: 2},
                    {x: 3, y: 1, width: 1, height: 2},
                    {x: 4, y: 1, width: 1, height: 1},
                    {x: 2, y: 3, width: 3, height: 1},
                    {x: 1, y: 4, width: 1, height: 1},
                    {x: 1, y: 3, width: 1, height: 1},
                    {x: 2, y: 4, width: 1, height: 1},
                    {x: 2, y: 5, width: 1, height: 1}
                ];

                this.grid = $('.grid-stack').data('gridstack');

                this.loadGrid = function () {
                    this.grid.removeAll();
                    var items = GridStackUI.Utils.sort(this.serializedData);
                    _.each(items, function (node) {
                        this.grid.addWidget($('<div><div class="grid-stack-item-content" /><div/>'),
                            node.x, node.y, node.width, node.height);
                    }, this);
                    return false;
                }.bind(this);

                this.saveGrid = function () {
                    this.serializedData = _.map($('.grid-stack > .grid-stack-item:visible'), function (el) {
                        el = $(el);
                        var node = el.data('_gridstack_node');
                        return {
                            x: node.x,
                            y: node.y,
                            width: node.width,
                            height: node.height
                        };
                    }, this);
                    $('#saved-data').val(JSON.stringify(this.serializedData, null, '    '));
                    return false;
                }.bind(this);

                this.clearGrid = function () {
                    this.grid.removeAll();
                    return false;
                }.bind(this);

                $('#save-grid').click(this.saveGrid);
                $('#load-grid').click(this.loadGrid);
                $('#clear-grid').click(this.clearGrid);

                this.loadGrid();
            };
        });
    </script>
</body>
</html>