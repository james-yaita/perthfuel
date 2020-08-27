/*
Script based on http://www.webtoolkit.info/sortable-html-table.html
*/


/* globals, document */

var DIR_UNKNOWN = 0,
    DIR_UP = 1,
    DIR_DOWN = 2;
	

function $(id) {
    "use strict";
    return document.getElementById(id);
}



function SortData(ele, category_info) {
    "use strict";
    var newSet = [],
        sortType = null,
        col_id = null,
        tableBody = $(ele),
        createImageTag = null,
        insertSortButtons = null,
        sortNumerically = null,
        sortAlphabetically = null,
        direction = null,
        updateImages = null,
        sort = null,
        sortOrder = DIR_UP,
        categories = category_info,
        asc_image = "static/media/asc.png",
        asc_alt = "Ascending Order",
        des_image = "static/media/des.png",
        des_alt = "Descending Order",
        unk_image = "static/media/unk.png",
        unk_alt = "Column not Sorted";


    
    /*
        Split address into sections by spaces
        Assumes elements after an element containing numbers
        provides the sort order.
        Covers 'Lot 5 Some Road', '101a Some Road'
        Use second element otherwise, as it likely to be 'Cnr some street and some highway'
    */
   
    /*this.sortByAddress = function (a, b) {
        
    };
*/
    insertSortButtons = function() {
    /*
      Inserts the code to activate a column sort
    */
        categories.forEach(category => {
            var output = "",
            inital_text = $(category.td_element_id).innerHTML;
            output += "<span ";
            output += "title=\"Click to sort\" "
            output += "onclick=\"javascript:sorter.sort('";
            output += category.name;
            output += "',";
            output += category.col_number;
            output += ")\">";
            output += inital_text;
            output += "&nbsp;"
            output += createImageTag(category.direction, category.img_element_id, inital_text);
            output += "</span>"
            $(category.td_element_id).innerHTML = output;
            
        });
        
    };
    
    createImageTag = function (direction, element_identifier, col_name) {
    /*
      Creates the image tag.  Use the direction to determine the image.
      Other parameters passed are used in the construction of the image attributes
    */
        var img_txt = "<img ";
        switch (direction) {
            case DIR_UP:
                img_txt += "src=\"" + asc_image + "\" alt=\"" +  asc_alt + "\"";
                break;
            case DIR_DOWN:
                img_txt += "src=\"" + des_image + "\" alt=\"" +  des_alt + "\"";
                break;
            default:
                img_txt += "src=\"" + unk_image + "\" alt=\"" +  unk_alt + "\"";
                
        }
        img_txt  += " id=\"" + element_identifier + "\"";
        img_txt += " title=\"Sort filter for " + col_name + "\"";
        img_txt += " height=\"15\" width=\"15\"";
        img_txt += "/>";
        
        return img_txt;
        
        
    };
    
    
    sortAlphabetically = function (col_id) {
        return function (a, b) {
            return a.getElementsByTagName("td")[col_id].innerHTML.toLowerCase().localeCompare(
                b.getElementsByTagName("td")[col_id].innerHTML.toLowerCase());
        };
    };

    sortNumerically = function (col_id) {
        return function (a, b) {
            return parseFloat(a.getElementsByTagName("td")[col_id].innerHTML) -
                parseFloat(b.getElementsByTagName("td")[col_id].innerHTML);
        };
    };

    
    direction = function (sortType) {

        var newDirection,
            elementName = null,
            cat = null;

        categories.forEach(cat => {
            if (sortType.match(cat.name)) {
                elementName = cat.img_element_id;
            }   
        });


        if ($(elementName).alt.match(asc_alt)) {
            $(elementName).src = des_image;
            $(elementName).alt = des_alt;
            newDirection = DIR_DOWN;
        } else {
            $(elementName).src = asc_image;
            $(elementName).alt = asc_alt;
            newDirection = DIR_UP;
        }
        
        updateImages(sortType);
        
        return newDirection;
    };
    
    
    updateImages = function (category_used_for_sorting) {
        /*
            Update the image for sort order for the columns
            not used for sorting.
            
            Make them a neutral state    
        */
        categories.forEach(category_column => {
            if (!category_used_for_sorting.match(category_column.name)) {
                if (category_column.img_element_id){
                    $(category_column.img_element_id).src = unk_image;
                    $(category_column.img_element_id).alt = unk_alt;                    
                }

            }   
        });
    };  // end updateImages
    
    //, newSortType, newColId
    sort = function (newSortType, newColId) {


		var counter = 0,
            sortfn = sortNumerically,
            sortType = newSortType,
            sortOrder = direction(sortType),
            cat = null,
            col_id = newColId,
            i = 0,
            j = 0;
        
        
        categories.forEach(cat => {
            if (sortType.match(cat.name)) {
                if (cat.sort_cat_function === "sortAlphabetically") {
                    sortfn = sortAlphabetically;
                    // TODO make the sort function pubically available
                }
            }   
        });
        
        for (var rowNum = 0; rowNum < tableBody.rows.length; rowNum += 1) {
            newSet[rowNum] = tableBody.rows[rowNum]
        }

        // sort the objects 
        newSet.sort(sortfn(col_id));
        
        if (sortOrder === DIR_DOWN) {
            newSet.reverse();
        }
        
        // Display it
        for (i = 0; i < newSet.length; i += 1) {
            tableBody.appendChild(newSet[i]);
        }

        
	
	}; // end sort
    
 

    insertSortButtons(); 
    
    return {
        "categories" : categories,
        "insertSortButtons" : insertSortButtons,
        "sort": sort,
        "sortAlphabetically" : sortAlphabetically,
        "sortNumerically" : sortNumerically
    }
}
    