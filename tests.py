from renamer import *

tests = ["In.The.Heart.of.the.Sea.2015.DVDScr.XVID.AC3.HQ.Hive-CM8", "Dracula Untold (2014)", "The.House.2017.1080p.WEB-DL.DD5.1.H264-FGT", "The.Magnificent.Seven.2016.720p.BRRip.x264.AAC-ETRG", "The.Mountain.Between.Us.2017.BRRip.XviD.AC3-EVO", "The.Signal.2014.1080p.BluRay.H264.AAC-RARBG", "Taken 3 2014 NEW SOURCE HDRip", "Sound.Of.My.Voice.2011.LIMITED.BDRip.XviD-ALLiANCE", "Sing 2016 1080p WEB-DL x264 AC3-JYK", "Silver.Linings.Playbook.2012.720p.BluRay.x264-iNFAMOUS [PublicHD]", "Resident Evil - The Final Chapter 2017 720p BrRip x264 - FUM", "Imperium.2016.720p.WEBRip.x264.AAC-ETRG.mp4"]


for name in tests:
    print("\n\n\n\n===============\n")
    print("TESTING: %s" % name)
    print("(%s) %s" % (get_year(name), get_name(name)))

    nm, year = fetch_movie(get_name(name), year=get_year(name))
    print("%s (%s)" % (nm, year))
