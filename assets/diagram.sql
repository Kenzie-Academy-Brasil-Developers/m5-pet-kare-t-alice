Table Pet {
  id int [primary key]
  name varchar
  age int
  weight float
  sex varchar
  group_id bigint
}

Ref: Pet.group_id > Group.id

Table Group {
  id int [primary key]
  scientific_name varchar
  created_at datetime
}

Table Trait_Pivot {
  id int [primary key]
  pet_id bigint
  trait_id bigint
}

Ref: Pet.id > Trait_Pivot.pet_id
Ref: Trait.id > Trait_Pivot.trait_id

Table Trait{
  id int [primary key]
  name varchar
  created_at datetime
}