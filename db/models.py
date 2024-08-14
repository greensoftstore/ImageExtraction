import sqlite3

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Document;")
    cursor.execute("DROP TABLE IF EXISTS Page;")
    cursor.execute("DROP TABLE IF EXISTS Rectangle;")

    # Create Document table
    cursor.execute('''
    CREATE TABLE Document (
        DocID INTEGER PRIMARY KEY AUTOINCREMENT,
        FileName VARCHAR(64) NOT NULL,
        FilePath VARCHAR(64) NOT NULL,
        Hashcode VARCHAR(64) NOT NULL,
        NumPages INTEGER NOT NULL,
        Height_px INTEGER NOT NULL,
        Width_px INTEGER NOT NULL
    );
    ''')

    # Create Page table
    cursor.execute('''
    CREATE TABLE Page (
        PageID INTEGER PRIMARY KEY AUTOINCREMENT,
        DocID INTEGER NOT NULL,
        PageNum INTEGER NOT NULL,
        LeftMargin INTEGER NOT NULL,
        RightMargin INTEGER NOT NULL,
        TopMargin INTEGER NOT NULL,
        BottomMargin INTEGER NOT NULL,
        FOREIGN KEY (DocID) REFERENCES Document(DocID)
    );
    ''')

    # Create Rectangle table
    cursor.execute('''
    CREATE TABLE Rectangle (
        RectID INTEGER PRIMARY KEY AUTOINCREMENT,
        PageID INTEGER NOT NULL,
        DocID INTEGER NOT NULL,
        XPos INTEGER NOT NULL,
        YPos INTEGER NOT NULL,
        Width INTEGER NOT NULL,
        Height INTEGER NOT NULL,
        Png VARCHAR(64) NOT NULL,
        LeftAligned CHAR(1) NOT NULL DEFAULT 'N',
        RightAligned CHAR(1) NOT NULL DEFAULT 'N',
        Centered CHAR(1) NOT NULL DEFAULT 'N',
        NumLines INTEGER NOT NULL,
        Paragraph_Type CHAR(1) NOT NULL,
        FirstLineIndent CHAR(1) NOT NULL DEFAULT 'N',
        LastLineIndent CHAR(1) NOT NULL DEFAULT 'N',
        MergedPrevRectID INTEGER NOT NULL DEFAULT 0,
        MergedNextRectID INTEGER NOT NULL DEFAULT 0,
        Text_OCR TEXT NOT NULL DEFAULT '',
        Text_pyPdf TEXT NOT NULL DEFAULT '',
        Text_Nougat TEXT NOT NULL DEFAULT '',
        Text_Consolidated TEXT NOT NULL DEFAULT '',
        Font_Size VARCHAR(64) NOT NULL DEFAULT '',
        Font_Family VARCHAR(64) NOT NULL DEFAULT '',
        Font_Bold CHAR(1) NOT NULL DEFAULT 'N',
        Font_Italic CHAR(1) NOT NULL DEFAULT 'N',
        FOREIGN KEY (PageID) REFERENCES Page(PageID),
        FOREIGN KEY (DocID) REFERENCES Document(DocID)
    );
    ''')

    conn.commit()