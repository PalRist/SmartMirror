$(
    function () {
        var options = {
            float: true
        };
        $('.grid-stack').gridstack(options);

        new function () {
            this.items = [
                {x: 0, y: 0, width: 2, height: 2},
                {x: 3, y: 1, width: 1, height: 2},
                {x: 4, y: 1, width: 1, height: 1},
                {x: 2, y: 3, width: 3, height: 1},
                {x: 2, y: 5, width: 1, height: 1}
            ];

            this.grid = $('.grid-stack').data('gridstack');

            this.grid.width = screen.width;
            this.grid.height = screen.height;

            this.addNewWidget = function () {
                var node = this.items.pop() || {
                        x: 1,
                        y: 1,
                        width: 1 + 3 * Math.random(),
                        height: 1 + 3 * Math.random()
                    };
                var el = this.grid.addWidget($('<div class="grid-stack-item"><div class="grid-stack-item-content">' + "10hi" + '</div></div>'), node.x, node.y, node.width, node.height, true);
                return false;
            }.bind(this);
            var self = this;
            function createWidget(event){
                var node = self.items.pop() || {
                        x: 1,
                        y: 1,
                        width: 1 + 3 * Math.random(),
                        height: 1 + 3 * Math.random()
                    };
                var el = self.grid.addWidget($('<div class="grid-stack-item"><div class="grid-stack-item-content">' + event.data.element + '</div></div>'), node.x, node.y, node.width, node.height, true);
                return false;

            }


            let elm = "<img src='http://www.readersdigest.ca/wp-content/uploads/2011/01/4-ways-cheer-up-depressed-cat.jpg' </img>" ;
            //$('#add-new-widget').click(this.addNewWidget);
            $('#add-new-widget').click({element: elm},createWidget);

        };
    });