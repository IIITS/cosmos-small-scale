$(document).ready(function(){
    var hideit = ['#faculty-view', '#batch-view-1','#batch-view-2', '#deadline-view'];
    for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();	
    }	
    $('#faculty-view').show();	
    $('#deadline-link').click(function(){
	for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();
	}
	$('#deadline-view').show();
	});
    $('#faculty-link').click(function(){
    for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();	
    }
    $('#faculty-view').show();	
    });
    $('#students-link').click(function(){
    for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();	
    }
    $('#students-view').show();
    });
    
    $('#submissions-link').click(function(){
    
    for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();	
    }
    $('#submissions-view').show();
    });  
    $('#batch-link-1').click(function(){
     for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();	
    }
    $('#batch-view-1').show();	
    });   
    $('#batch-link-2').click(function(){
     for(var i=0; i<hideit.length; i++){
    $(hideit[i]).hide();    
    }
    $('#batch-view-2').show();  
    });
});
