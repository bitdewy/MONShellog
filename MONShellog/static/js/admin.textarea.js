window.onload = function()
{
    // create the FCK Editor and replace the specific text area with it
    var oFCKeditor = new FCKeditor( 'id_body' ) ;
    oFCKeditor.Width = '60%';
    oFCKeditor.Height = '500';
    oFCKeditor.BasePath	= '/media/fckeditor/';
    oFCKeditor.ReplaceTextarea() ;
}

