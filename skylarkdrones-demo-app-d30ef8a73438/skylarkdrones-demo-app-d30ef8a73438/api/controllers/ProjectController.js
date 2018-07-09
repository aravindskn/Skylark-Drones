var anchor = require('anchor')
module.exports = {

	validate : function(req,res,create){
		req.checkBody('name', 'Name is required').notEmpty()
 		req.checkBody('name', 'Name should be 5 - 10 chars').isByteLength({min:5,max:10});
		var errors = req.validationErrors();

		if(errors) {
			throw ValidationException(errors)
		}
	},

	create : function(req,res,next){
		this.validate(req,res);

		ProjectEntity.create({
			name : req.body.name
		}).exec(function(err,result){
			
			if(err) throw new Error('Project nor created')
			res.send(200,{msg:'Project created'});		
		})
		
	},

	get : function(req,res,next){
		var page = req.query.page ? req.query.page : 0;

		async.parallel([
		    function(callback){
		    	ProjectEntity
		    		.find({})
		    		.skip(10*page)
					.limit(10)
		    		.exec(callback); 
			},
		    function(callback){ 
		    	ProjectEntity.count({}).exec(callback)
		    }
		], function(err,result){
				if(err) throw new Error('Failed to get Projects')

				return res.json({data : result[0],total:result[1]});
		});
	},

	getById : function(req,res,next){
		console.log(req.param)
		ProjectEntity.findOne().where({id:req.params.id}).exec(function(err, project) {
			if(err) throw new Error('Error getting project')
			if(!project) return res.status(404)
			return res.json(project);
		});
	},

	update : function(req,res,next){
		ProjectEntity.findOne().where({id:req.params.id}).exec(function(err, project) {
			if(err) throw new Error('Error getting project')
			project.name = req.body.name;
			project.save(function(err,result){
				if(err)  throw new Error('Unable to update project');
				res.json({msg:'Project Updated'})
			})
		});
	},

	delete: function(req,res,next){

		ProjectEntity.destroy({id:req.params.id}).exec(function(err, project) {
			if(err) throw new Error('Error getting project')

			res.json({msg:'Project Deleted'})
			
		});
	}
	
};