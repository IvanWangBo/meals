function lazyload(condition, holder) {
    this.collection = [];
    this.holder = holder || "http://pic42.photophoto.cn/20170213/0005018358833690_b.jpg";
    this.condition = condition ||
        function() {
            return true
        }
}
lazyload.prototype.add = function(nodeobject) {
    nodeobject.count = 0;
    this.collection.push(nodeobject)
};
lazyload.prototype.load = function() {
    var self = this;
    for (var i = 0; i < self.collection.length; i++) {
        var obj = self.collection[i];
        if (!obj.loaded) {
            if (self.condition(obj.node)) {
                obj.node.src = obj.imgurl;
                obj.node.onerror = function() {
                    var source = this.getAttribute("source");
                    if (source) {
                        if (obj.count >= 1) {
                            this.src = self.holder;
                            return
                        }
                        this.src = source;
                        obj.count++
                    } else {
                        this.src = self.holder
                    }
                };
                obj.node.onload = function() {
                    var _width = this.width,
                        _height = this.height,
                        p_width = this.parentNode.offsetWidth,
                        p_height = this.parentNode.offsetHeight,
                        img_percent = _width / _height,
                        parent_percent = p_width / p_height;
                    if (img_percent > parent_percent) {
                        var w = p_height * img_percent;
                        this.style.height = p_height + "px";
                        this.style.width = w + "px";
                        this.style.marginLeft = -(w - p_width) / 2 + "px";
                        this.style.marginTop = 0 + "px"
                    } else {
                        var h = p_width / img_percent;
                        this.style.height = h + "px";
                        this.style.width = p_width + "px";
                        this.style.marginTop = -(h - p_height) / 2 + "px";
                        this.style.marginleft = 0 + "px"
                    }
                };
                obj.loaded = true
            }
        }
    }
};

