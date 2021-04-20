import filecmp


#def print_diff_files(dcmp):
#     print(dir(dcmp))
#     for name in dcmp.diff_files:
#         #print("diff_file %s found in %s and %s" % (name, dcmp.left,
#         #      dcmp.right))
#         print ("Druid only: %s" %(dcmp.left_only))
#         print ()
#         print ("Imply only: %s" %(dcmp.right_only))
#     for sub_dcmp in dcmp.subdirs.values():
#         print_diff_files(sub_dcmp)

#imply druid
#druid_docs = "/Users/charlessmith/codebase/imply-druid/docs"
#oss druid
druid_docs = "/Users/charlessmith/codebase/druid/docs"
imply_druid = "/Users/charlessmith/codebase/imply-docs/docs/druid"


#dcmp = dircmp(druid_docs, imply_druid) 
#print_diff_files(dcmp) 

doc_diff = filecmp.dircmp(druid_docs, imply_druid,ignore=None, hide=None)
print ("*******************")
print ("Comparing docs")
print ("*******************")
print ("Druid only: %s" %doc_diff.left_only)
print ()
print ("Imply only: %s" %doc_diff.right_only)
print ()
doc_file_dif = filecmp.cmpfiles(druid_docs, imply_druid, doc_diff.common, shallow=True)
print ("Changed files: %s" %(str(doc_file_dif[1])))
for dir in doc_diff.common_dirs:
    dd = druid_docs + "/" + dir
    id = imply_druid +  "/" + dir
    dir_diff = filecmp.dircmp(dd, id,ignore=None, hide=None)
    print ("*******************")
    print ("Cmparing %s" %(dir))
    print ("*******************")
    print ("Druid only: %s" %dir_diff.left_only)
    print ()
    print ("Imply only: %s" %dir_diff.right_only)
    print ()
    print ()
    file_dif = filecmp.cmpfiles(dd, id, dir_diff.common, shallow=True)
    print ("Changed files: %s" %(str(file_dif[1])))



