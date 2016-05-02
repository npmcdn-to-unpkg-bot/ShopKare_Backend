(function() {
  var app = angular.module('ShopKare_Backend-master', []);
var base = 'http://127.0.0.1:5000';
  
  var categories = [];
  var level1keys= [];
    app.controller('add_new_product',function($scope,$http, Upload, $timeout){
      $scope.Product={};
      $scope.index1=0;
      $scope.Product.Quantity=[{"Quantity":["",""]}];
      $scope.product_id=$scope.level_1_category+$scope.level_2_category+$scope.level_3_category;
       $http.get("http://shopkare.com/api/Admin/addProduct?user="+JSON.stringify($scope.Product))
       .then(function(response){
        $scope.main_level_products=response['data'];
       });


       $scope.button_function=function(){
        console.log("Function Called Successfully");
        $scope.index1=$scope.index1+1;
      $scope.dataa={"Quantity": [" "," "]};
        $scope.Product.Quantity.push($scope.dataa);
       };
       
      $scope.addProduct = function()
      {
	$scope.Product['_id'] = id;
	$scope.Product['Level1 Category'] = JSON.parse($scope.l1category)._id;
	$scope.Product['Main Category'] = $scope.mainCategories[$scope.mainCategory];
	$scope.Product['Sub Category'] = $scope.subcategories[$scope.subcategoryindex];
	console.log(JSON.stringify($scope.Product));
      };
       $scope.gettablenames=function(){
        console.log("function Called Successfully");
       	$http.post("php/getTablename.php",{"category1":$scope.level_2_category})
       	.then(function(response){
       		$scope.getTablenames=response['data'];
                  console.log("php page Called Successfully");
       	})

       };
       
      $http.post(base+'/api/Admin/reteriveCategories/')
 	.success(function(data){
 	  categories = data;
	  level1keys = Object.keys(data)
	  for (key in level1keys)
	  {
	    level1keys[key] = data[key]._id;
	    console.log(data[key]._id);
	  }
	  
	  $scope.categories = categories;
	  console.log(data);
 	})
 	.error(function(err){
 	  console.log(err);
 	});
	$scope.mainCategories = [];
    $scope.selectLevel1Category = function()
    {
      $scope.mainCategories=[];
      var a = JSON.parse($scope.l1category);
      $scope.MainCategories = a.Categories; 
//       console.log(a.Categories);
      $scope.level1keys = Object.keys(a.Categories);
      
// 	console.log(Object.keys(a.Categories[]));
	for (key in $scope.level1keys)
	{
	  $scope.mainCategories.push(Object.keys(a.Categories[key])[0]);
	}
	console.log($scope.mainCategories);
    };
    
    $scope.selectmainCategory = function(){
      
      $scope.subcategories = JSON.parse($scope.l1category).Categories[$scope.mainCategory];
      var mainCategory = $scope.mainCategories[$scope.mainCategory]; 
      console.log($scope.subcategories[mainCategory]);
      $scope.subcategories = $scope.subcategories[mainCategory];
//       console.log(Object.keys(a.Categories[key])[0]);
    };
    var id = '';
    $scope.getproducts = function()
    {
      id = level1keys.indexOf(JSON.parse($scope.l1category)._id).toString() +'_'+ $scope.mainCategory.toString() + '_'+ $scope.subcategoryindex.toString();
      console.log(id);
    };
    
    });
})();
