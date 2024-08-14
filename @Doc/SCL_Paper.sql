--==============================================================
-- DBMS name:      ANSI Level 2
-- Created on:     7/10/2024 7:33:44 PM
--==============================================================


drop table if exists Document;

drop table if exists Page;

drop table if exists Rectangle;

--==============================================================
-- Table: Document
--==============================================================
create table Document (
DocID                INTEGER              not null,
FileName             VARCHAR(64)          not null,
FilePath             VARCHAR(64)          not null,
Hashcode             VARCHAR(64)          not null,
NumPages             INTEGER              not null,
Height_px            INTEGER              not null,
Width_px             INTEGER              not null
);

--==============================================================
-- Table: Page
--==============================================================
create table Page (
PageID               INTEGER              not null,
DocID                INTEGER              not null,
PageNum              INTEGER              not null,
LeftB                INTEGER              not null,
RightMargin          INTEGER              not null,
TopMargin            INTEGER              not null,
BottomMargin         INTEGER              not null
);

--==============================================================
-- Table: Rectangle
--==============================================================
create table Rectangle (
RectID               INTEGER              not null,
PageID               INTEGER              not null,
DocID                INTEGER              not null,
XPos                 INTEGER              not null,
YPos                 INTEGER              not null,
Width                INTEGER              not null,
Height               INTEGER              not null,
Png                  VARCHAR(64)          not null,
LeftAligned          CHAR(1)              not null default 'N',
RightAligned         CHAR(1)              not null default 'N',
Centered             CHAR(1)              not null default 'N',
NumLines             INTEGER              not null,
Paragraph_Type       CHAR(1)              not null,
FirstLineIndent      CHAR(1)              not null default 'N',
LastLineIndent       CHAR(1)              not null default 'N',
MergedPrevRectID     INTEGER              not null default 0,
MergedNextRectID     INTEGER              not null default 0,
Text_OCR             VARCHAR(64)          not null default '',
Text_pyPdf           VARCHAR(64)          not null default '',
Text_Nougat          VARCHAR(64)          not null default '',
Text_Consolidated    VARCHAR(64)          not null default ''
);

