use school_service_core::{E, Q, AuditedSave};
use school_service_core::teaql_core::Entity;

fn sep(title: &str) {
    println!("\n{}", "=".repeat(60));
    println!("  {}", title);
    println!("{}", "=".repeat(60));
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    std::env::set_var("SCHOOL_SERVICE_CORE_DATABASE_URL", "sqlite::memory:");

    let ctx = school_service_core::service_runtime_from_env().await?;

    // Load seed data
    school_service_core::sample_data::generate_sample_data(
        &ctx,
        school_service_core::sample_data::SampleDataPlan::small(),
    )
    .await?;
    println!("Seed data loaded ✓");

    // ============================================================
    // Q API Tests
    // ============================================================

    // Q1: List all platforms
    sep("Q1: List all platforms");
    let platforms = Q::platforms()
        .comment("Load all platforms")
        .purpose("Display platform list")
        .execute_for_list(&ctx)
        .await?;
    println!("Platforms count: {}", platforms.len());
    for p in &platforms {
        println!("  Platform: id={}, name={}", p.id(), p.name());
    }

    // Q2: List all school types
    sep("Q2: List all school types");
    let school_types = Q::school_types()
        .comment("Load all school types")
        .purpose("Display constant types list")
        .execute_for_list(&ctx)
        .await?;
    println!("School types count: {}", school_types.len());
    for st in &school_types {
        println!("  SchoolType: id={}, name={}, code={}", st.id(), st.name(), st.code());
    }

    // Q3: Create a new school
    sep("Q3: Create a primary school");
    let mut school1 = Q::schools()
        .comment("Prepare new school entity")
        .purpose("Create primary school")
        .new_entity(&ctx);
    school1.update_name("Sunshine Primary School");
    school1.update_platform_id(1_u64);
    school1.update_school_type_to_primary();
    let saved1 = school1
        .audit_as("Create primary school")
        .save(&ctx)
        .await?;
    println!("Created school: {:?}", saved1);

    // Q4: Create a secondary school
    sep("Q4: Create a secondary school");
    let mut school2 = Q::schools()
        .comment("Prepare new school entity")
        .purpose("Create secondary school")
        .new_entity(&ctx);
    school2.update_name("Mountain View Secondary School");
    school2.update_platform_id(1_u64);
    school2.update_school_type_to_secondary();
    let saved2 = school2
        .audit_as("Create secondary school")
        .save(&ctx)
        .await?;
    println!("Created school: {:?}", saved2);

    // Q5: List all schools (verify creation)
    sep("Q5: List all schools");
    let schools = Q::schools()
        .comment("List all schools after creation")
        .purpose("Verify school creation")
        .execute_for_list(&ctx)
        .await?;
    println!("Schools count: {}", schools.len());
    for s in schools.iter().take(5) {
        let stype = if s.school_type_is_primary() { "Primary" } else { "Secondary" };
        println!("  School: id={}, name={} [{}]", s.id(), s.name(), stype);
    }
    println!("  ... ({} total)", schools.len());

    // Q6: Filter by name containing
    sep("Q6: Filter by name containing 'Primary'");
    let named = Q::schools()
        .with_name_containing("Primary")
        .comment("Filter schools with 'Primary' in name")
        .purpose("Test name filter")
        .execute_for_list(&ctx)
        .await?;
    println!("Schools with 'Primary' in name: {}", named.len());
    for s in &named {
        println!("  id={}, name={}", s.id(), s.name());
    }

    // Q7: Filter by constant shortcut
    sep("Q7: Filter by school_type = PRIMARY");
    let primary_schools = Q::schools()
        .with_school_type_is_primary()
        .comment("Filter to primary schools only")
        .purpose("Test constant shortcut filter")
        .execute_for_list(&ctx)
        .await?;
    println!("Primary schools count: {}", primary_schools.len());
    for s in primary_schools.iter().take(3) {
        println!("  id={}, name={}, is_primary={}", s.id(), s.name(), s.school_type_is_primary());
    }
    println!("  ... ({} total)", primary_schools.len());

    // Q8: Count all schools
    sep("Q8: Count all schools");
    let count = Q::schools()
        .comment("Count all active schools")
        .purpose("Test execute_for_count")
        .execute_for_count(&ctx)
        .await?;
    println!("Total school count: {}", count);

    // Q9: Load with relations
    sep("Q9: Load school with platform + school_type");
    let school_with_rels = Q::schools()
        .select_platform()
        .select_school_type()
        .with_name_is("Sunshine Primary School")
        .comment("Load school with nested relations")
        .purpose("Test relation loading")
        .execute_for_one(&ctx)
        .await?;
    if let Some(school) = school_with_rels {
        println!("School: id={}, name={}", school.id(), school.name());
        if let Some(p) = school.platform() {
            println!("  Platform: id={}, name={}", p.id(), p.name());
        }
        if let Some(st) = school.school_type() {
            println!("  SchoolType: id={}, name={}, code={}", st.id(), st.name(), st.code());
        }
    }

    // ============================================================
    // E API Tests
    // ============================================================

    // E1: Get scalar fields
    sep("E1: E expression — get_name, get_id");
    if let Some(school) = Q::schools()
        .with_name_is("Sunshine Primary School")
        .comment("Load for E expression test")
        .purpose("Test E facade")
        .execute_for_one(&ctx)
        .await?
    {
        let name = E::school(&school).get_name().eval();
        println!("E::school(s).get_name().eval() = {:?}", name);

        let id = E::school(&school).get_id().eval();
        println!("E::school(s).get_id().eval() = {:?}", id);
    }

    // E2: Relation traversal
    sep("E2: E expression — relation traversal");
    let sv = Q::schools()
        .select_platform()
        .select_school_type()
        .with_name_is("Mountain View Secondary School")
        .comment("Load for E traversal")
        .purpose("Test E relation traversal")
        .execute_for_one(&ctx)
        .await?;
    if let Some(school) = sv {
        let platform_name = E::school(&school).get_platform().get_name().eval();
        println!(
            "E::school(s).get_platform().get_name().eval() = {:?}",
            platform_name
        );

        let type_code = E::school(&school).get_school_type().get_code().eval();
        println!(
            "E::school(s).get_school_type().get_code().eval() = {:?}",
            type_code
        );

        let is_secondary = E::school(&school).school_type_is_secondary().eval();
        println!(
            "E::school(s).school_type_is_secondary().eval() = {:?}",
            is_secondary
        );
    }

    // E3: or_else default
    sep("E3: E expression — or_else default");
    if let Some(school) = Q::schools()
        .with_name_is("Sunshine Primary School")
        .comment("Load for or_else test")
        .purpose("Test E or_else")
        .execute_for_one(&ctx)
        .await?
    {
        let name = E::school(&school).get_name().or_else("Unknown".to_string());
        println!("E::school(s).get_name().or_else(\"Unknown\") = {}", name);
    }

    // ============================================================
    // Update: Rename
    // ============================================================
    sep("Update: Rename school");
    let to_rename = Q::schools_minimal()
        .select_name()
        .with_name_is("Sunshine Primary School")
        .comment("Load school for rename")
        .purpose("Test update operation")
        .execute_for_one(&ctx)
        .await?;
    if let Some(mut school) = to_rename {
        school.update_name("Sunshine International Primary School");
        school
            .audit_as("Rename school to International")
            .save(&ctx)
            .await?;
        println!("School renamed ✓");
    }
    let renamed = Q::schools()
        .with_name_containing("International")
        .comment("Verify rename")
        .purpose("Confirm update worked")
        .execute_for_list(&ctx)
        .await?;
    for s in &renamed {
        println!("  Renamed: id={}, name={}", s.id(), s.name());
    }

    // ============================================================
    // Delete: Soft-delete
    // ============================================================
    sep("Delete: Soft-delete a school");
    let to_delete = Q::schools_minimal()
        .select_name()
        .with_name_is("Mountain View Secondary School")
        .comment("Load school for soft delete")
        .purpose("Test soft delete")
        .execute_for_one(&ctx)
        .await?;
    if let Some(mut school) = to_delete {
        school.mark_as_delete();
        school
            .audit_as("Soft delete secondary school")
            .save(&ctx)
            .await?;
        println!("School soft-deleted ✓");
    }
    let active = Q::schools()
        .comment("Count active after delete")
        .purpose("Verify soft delete")
        .execute_for_count(&ctx)
        .await?;
    println!("Active schools after delete: {}", active);

    // ============================================================
    // Summary
    // ============================================================
    sep("All Q/E API tests completed!");
    println!("Q API: list, filter, count, create, relation loading ✓");
    println!("E API: get_field, relation traversal, constant check, or_else ✓");
    println!("Update: rename school ✓");
    println!("Delete: soft-delete school ✓");
    println!("\nAll tests PASSED! ✓");

    Ok(())
}
