var app = angular.module('Shopkare', ['ui.router','Shopkare.controllers','ui.bootstrap', 'toastr']);


app.config(function($stateProvider, $urlRouterProvider, toastrConfig) {
  $urlRouterProvider.otherwise('/grocery/home/products');
  $stateProvider

    .state('index',{
      url : '/index',
      'templateUrl' : 'static/partial-index.html',
      'controller' : 'indexController'
    })

    .state('home',{
      url : '/home',
      views: {

          '': { templateUrl: 'static/home.html' },

          'header@home': { 
            templateUrl : 'static/templates/header.html',
            controller : 'headerController'
          },

          'footer@home': { 
            templateUrl : 'static/templates/footer.html',
            controller : 'footerController'
          },

          'products@home': { 
            templateUrl : 'static/templates/indexProduct.html',
            controller : 'productsMainController'
          },

          'sidebar@home': { 
            templateUrl : 'static/templates/sidebar.html',
            controller : 'sidebarController'
          },

          'dropdownmenu@home': { 
            templateUrl : 'static/templates/dropdownMenu.html',
            controller : 'dropdownMenuController'
          }
        },

        controller : 'homeController'
    })

    .state('grocery',{
      url : '/grocery',
      views: {

          '': { templateUrl: 'static/home.html' },

          'header@grocery': { 
            templateUrl : 'static/templates/header.html',
            controller : 'headerController'
          },

          'footer@grocery': { 
            templateUrl : 'static/templates/footer.html',
            controller : 'footerController'
          },

         'content@grocery': {
            templateUrl : 'static/templates/content.html',
            controller : ''
          }
        },
        controller : 'groceryController'
    })
    .state('grocery.home',{
      url : '/home',
      views: {
         'sidebar@grocery': {
            templateUrl : 'static/templates/sidebar.html',
            controller : 'sidebarController'
          },

          'dropdownmenu@grocery': { 
            templateUrl : 'static/templates/dropdownMenu.html',
            controller : 'dropdownMenuController'
          }
        },
        controller : 'groceryController'
    })
    .state('grocery.home.products',{
      url : '/products',
      views: {
          'products@grocery': { 
            templateUrl : 'static/templates/groceryProduct.html',
            controller : 'productsGroceryController'
          }
        }
    })
    .state('grocery.home.search',{
      url : '/search?query',
      views: {
          'products@grocery': { 
            templateUrl : 'static/templates/searchProduct.html',
            controller : 'searchController'
          }
        }
    })
    .state('grocery.home.CategoryProducts',{
      url : '/categoryproducts?level1Category&mainCategory',
      views: {
          'products@grocery': { 
            templateUrl : 'static/templates/CategoryProducts.html',
            controller : 'CategoryProductsController'
          }
        }
    })
    .state('grocery.home.SubCategoryProducts',{
      url : '/subcategoryproducts?level1Category&mainCategory&subcategory',
      views: {
          'products@grocery': { 
            templateUrl : 'static/templates/SubCategoryProducts.html',
            controller : 'SubCategoryProductsController'
          }
        }
    })
    .state('grocery.home.AllSubCategoryProducts',{
      url : '/allsubcategoryproducts?level1Category&mainCategory&subcategory',
      views: {
          'products@grocery': {
            templateUrl : 'static/templates/allSubCategoryProducts.html',
            controller : 'AllSubCategoryProductsController'
          }
        }
    })
    .state('grocery.home.Product',{
      url : '/product:product',
      views: {
        'products@grocery': {
          templateUrl : 'static/templates/productdetails.html',
          controller : 'ProductDetailsController'
        }
      }
    })

    .state('stationary',{
      url : '/stationary',
      views: {

          '': { templateUrl: 'static/home.html' },

          'header@stationary': { 
            templateUrl : 'static/templates/header.html',
            controller : 'headerController'
          },

          'footer@stationary': { 
            templateUrl : 'static/templates/footer.html',
            controller : 'footerController'
          },

         'sidebar@stationary': { 
            templateUrl : 'static/templates/sidebar.html',
            controller : 'sidebarController'
          },

          'dropdownmenu@stationary': { 
            templateUrl : 'static/templates/dropdownMenu.html',
            controller : 'dropdownMenuController'
          },
        
          'products@stationary': { 
            templateUrl : 'static/templates/groceryProduct.html',
            controller : 'productsStationaryController'
          }
        },


        controller : 'stationaryController'
    })

    .state('courier',{
      url : '/courier',
      views: {

          '': { templateUrl: 'static/home.html' },

          'header@courier': { 
            templateUrl : 'static/templates/header.html',
            controller : 'headerController'
          },

          'footer@courier': { 
            templateUrl : 'static/templates/footer.html',
            controller : 'footerController'
          },

         'sidebar@courier': { 
            templateUrl : 'static/templates/sidebar.html',
            controller : 'sidebarController'
          },

          'dropdownmenu@courier': { 
            templateUrl : 'static/templates/dropdownMenu.html',
            controller : 'dropdownMenuController'
          },

          'products@courier': { 
            templateUrl : 'static/templates/courierProduct.html',
            controller : 'productsCourierController'
          }
        },

        controller : 'courierController'
    })


    .state('medicine',{
      url : '/medicine',
      views: {

          '': { templateUrl: 'static/templates/medicine.html' },

          'header@medicine': { 
            templateUrl : 'static/templates/header.html',
            controller : 'headerController'
          },

          'footer@medicine': { 
            templateUrl : 'static/templates/footer.html',
            controller : 'footerController'
          },

         'sidebar@medicine': { 
            templateUrl : 'static/templates/sidebar.html',
            controller : 'sidebarController'
          },

          'dropdownmenu@medicine': { 
            templateUrl : 'static/templates/dropdownMenu.html',
            controller : 'dropdownMenuController'
          }
        },

        controller : 'medicineController'
    })

   .state('cart',{
      url : '/cart',
      views: {
          '': { templateUrl: 'static/templates/cart.html'},

          'header@cart': { 
            templateUrl : 'static/templates/header.html',
            controller : 'headerController'
          },

          'footer@cart': { 
            templateUrl : 'static/templates/footer.html',
            controller : 'footerController'
          },
        },
      controller : 'cartController'
    })
   
   .state('checkout',{
      url : '/checkout',
      views: {
          '': { templateUrl: 'static/templates/cart.html'},

          'header@cart': { 
            templateUrl : 'static/templates/header.html',
            controller : 'headerController'
          },

          'footer@cart': { 
            templateUrl : 'static/templates/footer.html',
            controller : 'footerController'
          },
        },
      controller : 'cartController'
    })
   
   .state('contact',{
      url : '/contact',
      views: {
          '': { templateUrl: 'static/templates/contact-us.html'},

          'header@contact': { 
            templateUrl : 'static/templates/header.html',
            controller : 'headerController'
          },

          'footer@contact': { 
            templateUrl : 'static/templates/footer.html',
            controller : 'footerController'
          },
        },
      controller : 'contactController'
    });

    angular.extend(toastrConfig, {
      positionClass: 'toast-top-center',
      preventOpenDuplicates: true,
      timeOut: 5000
    });
  });