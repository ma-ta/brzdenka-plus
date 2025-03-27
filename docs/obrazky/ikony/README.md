# Your Favicon Package

This package was generated with [RealFaviconGenerator](https://realfavicongenerator.net/) [v0.16](https://realfavicongenerator.net/change_log#v0.16)

## Install instructions

To install this package:

Extract this package in <code>&lt;web site&gt;/obrazky/favicon/</code>. If your site is <code>http://www.example.com</code>, you should be able to access a file named <code>http://www.example.com/obrazky/favicon/favicon.ico</code>.

Insert the following code in the `head` section of your pages:

    <link rel="manifest" href="manifest.webmanifest">
    
    
    <!-- ikony, barvy -->
    <link rel="icon" type="image/png" sizes="16x16" href="obrazky/ikony/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="obrazky/ikony/favicon-32x32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="obrazky/ikony/apple-touch-icon.png">
    <link rel="mask-icon" href="obrazky/ikony/safari-pinned-tab.svg" color="#ffc40d">
    <link rel="shortcut icon" href="obrazky/ikony/favicon.ico">
    
    <meta name="msapplication-TileColor" content="#ffc40d">
    <meta name="msapplication-config" content="obrazky/ikony/browserconfig.xml">
    <meta name="theme-color" content="#333333">
    <!-- / ikony, barvy -->

*Optional* - Check your favicon with the [favicon checker](https://realfavicongenerator.net/favicon_checker)