var themePark = {};

$( document ).ready(function() {
    
    // defines the username value with the login username
    $('span.blue.username').text(Dashboards.context['user']);

});


// setting to add to bar charts which have labels over the bars
themePark.barChartLabel = function() {
    var cd = this.chartDefinition;
    
    cd.label_call = function() {
        // Add a label below the value label to show the category
        this.add(pv.Label)
            .font('lighter 12px "Open Sans"')
            .text(function(s){ return s.getSeriesLabel(); })
            .textBaseline('bottom')
            .textStyle('#676767')
            
            .textMargin(22);
    };
    
    cd.contentMargins = "28 0 0 0";
    
    // Values
    cd.valuesVisible = true;
    cd.valuesAnchor =  "top";
    cd.valuesFont = "14px Open Sans";
    
    cd.label_textStyle = "#343E47";
    cd.label_textBaseline = "bottom";
    
    cd.label_textMargin = 5;
    
}