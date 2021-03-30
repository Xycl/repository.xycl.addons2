#! /usr/bin/python

""" addons.xml generator """

import os
import hashlib


class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """
    def __init__( self ):
        # generate files
        self._generate_addons_file()
        self._generate_md5_file()
        # notify user
        print ("Finished updating addons xml and md5 files")

    def _generate_addons_file( self ):
        # addon list
        addons = os.listdir( "." )
        # final addons text
        addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"
        # loop thru and add each addons addon.xml file
        for addon in addons:
            try:
                # skip any file or .svn folder
                if ( not os.path.isdir( addon ) or addon == ".svn" ): continue
                # create path
                _path = os.path.join( addon, "addon.xml" )
                # split lines for stripping
                print("4")
                xml_lines = open( _path, encoding="utf8" ).read().splitlines()
                print("5")
                # new addon
                addon_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if ( line.find( "<?xml" ) >= 0 ): continue
                    # add line
                    addon_xml += line.rstrip() + "\n"
                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
            except Exception as e:
                # missing or poorly formatted addon.xml
                print ("Excluding %s for %s" % ( _path, e, ))
        # clean and add closing tag
        addons_xml = addons_xml.strip() + u"\n</addons>\n"
        # save file
        self._save_file( addons_xml, file="addons.xml" )

    def _generate_md5_file( self ):
        try:
            # create a new md5 hash
            print("3")
            m = hashlib.md5( open( "addons.xml", encoding="utf8" ).read().encode('utf-8') ).hexdigest()
            # save file
            self._save_file( m, file="addons.xml.md5" )
        except Exception as e:
            # oops
            print ("An error occurred creating addons.xml.md5 file!\n%s" % ( e, ))

    def _save_file( self, data, file ):
        try:
            # write data to the file
            print("1")
            open( file, "w" , encoding="utf8").write( data )
            print("2")
        except Exception as e:
            # oops
            print ("An error occurred saving %s file!\n%s" % ( file, e, ))


if ( __name__ == "__main__" ):
    # start
    Generator()
