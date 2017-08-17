
var PollForm = React.createClass({

	getInitialState: function(){
		return {title:'', option:'', options:[]};
	},

	handleTitleChange: function(e){
		this.setState({title: e.target.value});
	},

	handleOptionChange: function(e){
		this.setState({option: e.target.value});
	},

	handleOptionAdd: function(e){
		this.setState({
			options: this.state.options.concat({name: this.state.option}),
			option: ''
		});
	},

	handleSubmit: function(e){
		// TODO -- enable form submission
		e.preventDefault();
	},

	render: function(){
		return (
			<div className="card col-md-4 m-auto p-5">
		      <form id="poll_form" className="form-signin" onSubmit={this.handleSubmit}>
		        <h2 className="form-signin-heading">Create a poll</h2>

		        <div className="form-group has-success">
		          <label htmlFor="title" className="sr-only">Title</label>
		          <input type="text" id="title" name="title" className="form-control" placeholder="Title" onChange={this.handleTitleChange} required autoFocus />
		        </div>

		        <div className="form-group has-success">
		          <label htmlFor="option" className="sr-only">Option</label>
		          <input type="text" id="option" name="option" className="form-control" placeholder="Option" onChange={this.handleOptionChange}  required autoFocus />
		        </div>

		        <div className="form-group">
		          <button className="btn btn-lg btn-success btn-block" onClick={this.handleOptionAdd}>Add option</button>
		          <button className="btn btn-lg btn-success btn-block" type="submit">Save poll</button>
		        </div>
		        <br />
		      </form>
		      <h3>Live Preview</h3>
		      <br />
		      <LivePreview title={this.state.title} options={this.state.options} />
		    </div>
		);
	}
});

var LivePreview = React.createClass({
  	
	handleSampleVote: function(e){
		e.preventDefault();
	},

	render: function(){
    	
    	var options = this.props.options.map(function(option){
    		if (option.name) {
    			return(
    				<div key={option.name}>
    					<input name="options" type="radio" value={option.name} />
    					{option.name}
    					<br />
    				</div>
    			);
    		}
    	});

	    return(
	      <div className="panel panel-success">
	        <div className="panel-heading">
	          <h4>{this.props.title}</h4>
	        </div>
	        <div className="panel-body">
	          <form>
	            {options}
	            <br />
	            <button className="btn btn-success btn-outline hvr-grow" onClick={this.handleSampleVote}>Vote!</button>
	          </form>
	        </div>
	      </div>
	    );
  	}
});

ReactDOM.render(
	<PollForm />,
	document.getElementById('polls-form')
);
