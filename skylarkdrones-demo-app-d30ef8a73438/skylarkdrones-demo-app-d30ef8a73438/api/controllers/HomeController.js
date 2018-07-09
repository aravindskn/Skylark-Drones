module.exports =  {
    index: function (req, res) {
        res.view();
    },
    app:function(req,res){
      res.view({layout:'angular-layout',view:'app'});
    },
}

