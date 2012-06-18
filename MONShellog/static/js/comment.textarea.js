window.onload = function()
{
    // create the FCK Editor and replace the specific text area with it
    var oFCKeditor = new FCKeditor( 'id_comment' ) ;
    oFCKeditor.ToolbarSet = 'Basic' ;
    oFCKeditor.BasePath	= '/media/fckeditor/';
    oFCKeditor.ReplaceTextarea() ;
}

