# -*- coding: utf-8 -*-

html = '''
<html> 
<head> 
 <meta http-equiv="Content-Type" content="text/html;charset=utf-8" /> 
 <title>PlanetZope.org - Zope related news</title> 
 <link rel="stylesheet" type="text/css"
       href="./static/zpt_stylesheet.css" /> 
 <link rel="stylesheet" type="text/css"
       href="./static/zpt_custom.css" /> 
 <link rel="stylesheet" type="text/css"
       href="./static/planetzope.css" /> 
 <meta http-equiv="imagetoolbar" content="no" /> 
 <meta name="thanks" content="thanks to all who care - be zoped!" /> 
 <link rel="alternate" type="application/rss+xml" title="Planet Zope News" href="http://planet.zope.org/planet_rss10.xml" /> 
 <link rel="alternate" type="application/rss+xml" title="Planet Zope News" href="http://planetzope.org/ZopeNews/feed_rss.xml" /> 
 <link rel="shortcut icon"
       href="./static/favicon.ico" /> 
 <link rel="meta" type="application/rdf+xml" title="FOAF" href="http://zope.org/Members/d2m/foaf.rdf" />
 <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
 <script type="text/javascript">
    $(document).ready(function(){
        $("div.toggle").click(function(event){
            var entryid = $(this).attr('id');
            var content = $(this).text();
            $('div.'+entryid).toggle();
            if (content === '+') {
                $(this).text('-') }
            else {
                $(this).text('+') };
            $(this).addClass('entryseen');
        });
    });
 </script>
</head> 
 
<body class="PlanetZope">  

<div class="container_12 header">
    <div id="PortalDescription" class="grid_9 ">
        <br />PlanetZope aggregates
        the weblogs and product 
        announcements of Zope 
        related websites. 
        Contact <a href="http://blog.d2m.at/about">d2m</a>
    </div>
    <div id="timenow" class="grid_3">
        <br />%s
    </div>
</div>
<div class="container_12 masthead">
    <div id="PortalTitle" class="grid_12 ">
        <br />
        <a href="http://planetzope.org/">Planet Zope</a>
        <br />
    </div>
    <div id="PortalTagline" class="grid_12 ">
        <br /><br /><br />
        <a href="http://planetzope.org/">Zope related news</a>
    </div>
</div>
<div id="content" class="container_12">
    <div id="entries" class="grid_9 ">
    %s
    </div>
    <div id="sidebar" class="grid_3 ">
        <br /><br />
<script src="http://widgets.twimg.com/j/2/widget.js"></script>
<script>
new TWTR.Widget({
  version: 2,
  type: 'search',
  search: '#zope',
  interval: 6000,
  title: '#zope',
  subject: '',
  width: 'auto',
  height: 300,
  theme: {
    shell: {
      background: '#8ec1da',
      color: '#ffffff'
    },
    tweets: {
      background: '#ffffff',
      color: '#444444',
      links: '#1985b5'
    }
  },
  features: {
    scrollbar: true,
    loop: false,
    live: true,
    hashtags: true,
    timestamp: true,
    avatars: true,
    toptweets: false,
    behavior: 'all'
  }
}).render().start();
</script>
<br /><br />
        <div><br /><strong>Blogroll</strong></div>
        <div><a href="./aggregator.txt">a listing of all aggregated feeds</a></div>
        <div><br /><br /><strong>PlanetZope is a filtering aggregator</strong>, 
        current keywords are <code>%s</code>.
        </div>
</div>
<div class="container_12">
    <div id="footer" class="grid_12 ">
        &copy; 2011 <a href="http://d2m.at">d2m</a> | <a href="http://blog.planetzope.org">blog.planetzope.org</a>
    </div>
</div>
</body>
</html>
'''

rdf_item = '''<item rdf:about="%(link)s">
  <title><![CDATA[%(title)s]]></title>
  <link>%(link)s</link>
  <description><![CDATA[%(content)s]]></description>
  %(subjects)s
  <dc:creator>%(feedtitle)s</dc:creator>
  %(dcdate)s
</item>'''

rdf = '''<?xml version="1.0"?>

<rdf:RDF
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:dc="http://purl.org/dc/elements/1.1/"
xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
xmlns="http://purl.org/rss/1.0/"
>
<channel rdf:about="http://planet.zope.org">
<title>Planet Zope.org</title>
<link>http://planet.zope.org</link>
<description>
Zope related news
</description>

<image rdf:resource="http://www.zope.org/logo.png" />
<sy:updatePeriod>hourly</sy:updatePeriod>
<sy:updateFrequency>1</sy:updateFrequency>
<sy:updateBase>2006-08-27T07:38:03Z</sy:updateBase>

<items>
<rdf:Seq>
%s
</rdf:Seq>
</items>
</channel>

%s

</rdf:RDF> 
'''

entry_content = '''<div class="entry">
            <div class="entrytitle"><div id="entry%(counter)s" class="toggle">+</div><strong><a href="%(link)s">%(title)s</a></strong></div>
            <div class="feedinfo"><em>%(since)s by</em> <a href="%(feedlink)s">%(feedtitle)s</a></div>
            <div class="entrytext entry%(counter)s"><blockquote>%(content)s</blockquote></div>
            </div>'''

entry_nocontent = '''<div class="entry">
            <div class="entrytitle"><div class="notoggle">&nbsp;</div><strong><a href="%(link)s">%(title)s</a></strong></div>
            <div class="feedinfo"><em>%(since)s by</em> <a href="%(feedlink)s">%(feedtitle)s</a></div>
            <div class="entrytext"><blockquote>%(content)s</blockquote></div>
            </div>'''

blogroll = '''planetzope.org is a filtering feed aggregator.
----------------------------------------------
Contact http://blog.d2m.at/about for more information and requests.

Currently these feeds are fetched and filtered for %s


'''

